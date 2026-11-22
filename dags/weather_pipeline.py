from datetime import datetime

from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

PROJECT = "/opt/airflow/project"
PY = "/opt/airflow/pipeline-venv/bin/python"
DBT = "/opt/airflow/pipeline-venv/bin/dbt"

with DAG(
    dag_id="weather_pipeline",
    start_date=datetime(2026, 11, 1),
    schedule="@daily",
    catchup=False,
    tags=["weather", "etl"],
) as dag:

    extract = BashOperator(
        task_id="extract",
        bash_command=f"cd {PROJECT} && {PY} src/extract.py",
    )

    load = BashOperator(
        task_id="transform_and_load",
        bash_command=f"cd {PROJECT} && {PY} src/load.py",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {PROJECT}/dbt_weather && {DBT} run --profiles-dir . --project-dir .",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {PROJECT}/dbt_weather && {DBT} test --profiles-dir . --project-dir .",
    )

    extract >> load >> dbt_run >> dbt_test