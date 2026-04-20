# PulseCheck - Snowflake Data Loader
# Reads raw CSVs from data/raw/, deduplicates, and loads into Snowflake

import pandas as pd
import glob
from snowflake.connector.pandas_tools import write_pandas
from snowflake_connector import get_snowflake_connection
from config import RAW_DATA_PATH


def load_all_raw_files():
    """
    Reads all obesity CSVs, combines them, drops duplicate rows,
    then writes the clean result to Snowflake RAW_OBESITY (replacing
    whatever was there before).
    """
    print("🏥 PulseCheck - Snowflake Loader")
    print("=" * 50)

    conn = get_snowflake_connection()
    if not conn:
        return

    try:
        csv_files = glob.glob(f"{RAW_DATA_PATH}obesity_*.csv")

        if not csv_files:
            print("⚠️  No CSV files found in data/raw/")
            return

        print(f"📁 Found {len(csv_files)} file(s) to load")

        # Read and combine all CSV files into one DataFrame
        frames = []
        for filepath in csv_files:
            df = pd.read_csv(filepath, dtype=str)
            df.columns = [col.upper() for col in df.columns]
            df = df.drop_duplicates()  # Remove duplicate rows before loading
            frames.append(df)
            print(f"   📄 Read {len(df):,} rows from {filepath.split('/')[-1]}")

        combined = pd.concat(frames, ignore_index=True)
        before = len(combined)

        # Drop exact duplicate rows before loading
        combined = combined.drop_duplicates()
        removed = before - len(combined)

        if removed > 0:
            print(f"\n🧹 Removed {removed:,} duplicate rows ({before:,} → {len(combined):,})")
        else:
            print(f"\n✅ No duplicates found")

        # Load the clean, deduplicated data into Snowflake
        print(f"📤 Loading {len(combined):,} rows into Snowflake...")
        success, _, num_rows, _ = write_pandas(
            conn=conn,
            df=combined,
            table_name="RAW_OBESITY",
            auto_create_table=True,
            overwrite=True,
        )

        print("\n" + "=" * 50)
        if success:
            print(f"📊 Done! {num_rows:,} clean rows now in Snowflake RAW_OBESITY table")
        else:
            print("❌ Load failed")

    finally:
        conn.close()
        print("✅ Connection closed")


if __name__ == "__main__":
    load_all_raw_files()
