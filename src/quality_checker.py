# PulseCheck - Data Quality Checker
# Queries RAW_OBESITY from Snowflake and checks for data problems

import pandas as pd
from snowflake_connector import get_snowflake_connection
from config import QUALITY_THRESHOLDS

# The columns most important to have populated for analysis
KEY_COLUMNS = [
    "YEARSTART", "YEAREND", "LOCATIONABBR", "LOCATIONDESC",
    "QUESTION", "DATA_VALUE", "DATA_VALUE_TYPE",
    "STRATIFICATIONCATEGORY1", "STRATIFICATION1",
]


def fetch_table(conn, table_name="RAW_OBESITY"):
    """Pulls the full table from Snowflake into a pandas DataFrame."""
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    cols = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    return pd.DataFrame(rows, columns=cols)


def check_row_count(df):
    """Fails if the table has fewer rows than our minimum threshold."""
    count = len(df)
    minimum = QUALITY_THRESHOLDS["min_row_count"]
    passed = count >= minimum
    status = "✅" if passed else "❌"
    print(f"  {status} Row count: {count:,} (minimum: {minimum:,})")
    return passed


def check_nulls(df):
    """Fails if any key column exceeds the maximum allowed null percentage."""
    max_pct = QUALITY_THRESHOLDS["max_null_percentage"]
    all_passed = True

    for col in KEY_COLUMNS:
        if col not in df.columns:
            continue
        null_pct = (df[col].isna() | (df[col] == "")).sum() / len(df) * 100
        passed = null_pct <= max_pct
        if not passed:
            all_passed = False
        status = "✅" if passed else "❌"
        print(f"  {status} {col}: {null_pct:.1f}% nulls (max allowed: {max_pct}%)")

    return all_passed


def check_duplicates(df):
    """Fails if the percentage of duplicate rows exceeds the threshold."""
    max_pct = QUALITY_THRESHOLDS["max_duplicate_percentage"]
    total = len(df)
    duplicate_count = total - len(df.drop_duplicates())
    dup_pct = duplicate_count / total * 100
    passed = dup_pct <= max_pct
    status = "✅" if passed else "❌"
    print(f"  {status} Duplicates: {dup_pct:.1f}% ({duplicate_count:,} rows) (max allowed: {max_pct}%)")
    return passed


def run_quality_checks(table_name="RAW_OBESITY"):
    """
    Main entry point. Runs all three checks and prints a final verdict.
    Returns a dict of check name → True/False.
    """
    print("🔍 PulseCheck - Data Quality Checker")
    print("=" * 50)

    conn = get_snowflake_connection()
    if not conn:
        return

    try:
        print(f"📊 Checking table: {table_name}")
        df = fetch_table(conn, table_name)
        print(f"   Loaded {len(df):,} rows, {len(df.columns)} columns\n")

        results = {}

        print("📋 Row Count Check:")
        results["row_count"] = check_row_count(df)

        print("\n📋 Null Check (key columns):")
        results["nulls"] = check_nulls(df)

        print("\n📋 Duplicate Check:")
        results["duplicates"] = check_duplicates(df)

        print("\n" + "=" * 50)
        if all(results.values()):
            print("🎉 ALL CHECKS PASSED — data looks healthy!")
        else:
            failed = [k for k, v in results.items() if not v]
            print(f"⚠️  ISSUES FOUND: {', '.join(failed)}")

        return results

    finally:
        conn.close()
        print("✅ Connection closed")


if __name__ == "__main__":
    run_quality_checks()
