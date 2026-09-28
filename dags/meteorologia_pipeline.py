from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "data-engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}


with DAG(
    dag_id="weather_pipeline",
    default_args=default_args,
    description="Pipeline meteorológico para ciudades colombianas",
    start_date=datetime(2026, 9, 28),
    schedule=None,
    catchup=False,
    tags=["meteorologia", "open-meteo"],
) as dag:

    extract_weather = BashOperator(
        task_id="extract_weather",
        bash_command="python -m src.extract",
    )

    transform_weather = BashOperator(
        task_id="transform_weather",
        bash_command="python -m src.transform",
    )

    load_parquet = BashOperator(
        task_id="load_parquet",
        bash_command="python -m src.load",
    )

    extract_weather >> transform_weather >> load_parquet