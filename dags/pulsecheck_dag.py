from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess
import sys
import os

# Default settings for every task in the DAG
default_args = {
    'owner': 'snehitha',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id='pulsecheck_pipeline',
    default_args=default_args,
    description='Daily CDC data quality pipeline',
    schedule_interval='0 6 * * *',  # runs every day at 6am
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['pulsecheck', 'cdc', 'data-quality'],
) as dag:

    def fetch_cdc_data():
        """Fetch real CDC obesity data."""
        print("Starting CDC data fetch...")
        sys.path.insert(0, '/opt/airflow/src')
        from cdc_fetcher import fetch_cdc_data as fetch
        fetch()
        print("CDC data fetch complete.")

    def load_to_snowflake():
        """Load fetched data into Snowflake."""
        print("Loading data to Snowflake...")
        sys.path.insert(0, '/opt/airflow/src')
        from snowflake_loader import load_data
        load_data()
        print("Snowflake load complete.")

    def run_dbt_models():
        """Run dbt transformations."""
        print("Running dbt models...")
        result = subprocess.run(
            ['dbt', 'run', '--project-dir', '/opt/airflow/pulsecheck_dbt'],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            raise Exception(f"dbt run failed: {result.stderr}")
        print("dbt models complete.")

    def run_quality_checks():
        """Run data quality validation."""
        print("Running quality checks...")
        sys.path.insert(0, '/opt/airflow/src')
        from quality_checker import run_checks
        results = run_checks()
        print(f"Quality check results: {results}")
        print("Quality checks complete.")

    def send_alerts():
        """Send alerts if quality checks failed."""
        print("Checking if alerts need to be sent...")
        sys.path.insert(0, '/opt/airflow')
        from alert_system import check_and_alert
        # In production this would read results from previous task
        print("Alert check complete.")

    # Define tasks
    task_fetch = PythonOperator(
        task_id='fetch_cdc_data',
        python_callable=fetch_cdc_data,
    )

    task_load = PythonOperator(
        task_id='load_to_snowflake',
        python_callable=load_to_snowflake,
    )

    task_dbt = PythonOperator(
        task_id='run_dbt_models',
        python_callable=run_dbt_models,
    )

    task_quality = PythonOperator(
        task_id='run_quality_checks',
        python_callable=run_quality_checks,
    )

    task_alerts = PythonOperator(
        task_id='send_alerts',
        python_callable=send_alerts,
    )

    # Define the order of execution
    task_fetch >> task_load >> task_dbt >> task_quality >> task_alerts