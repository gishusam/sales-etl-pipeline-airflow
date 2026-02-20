# type: ignore
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from ingestion.extraction import extract_data
from ingestion.transformation import transform_and_load


default_args = {
    "owner": "airflow",
    "start_date": datetime(2026, 1, 15),
    "retries": 1,
}


# ---------------------------
# Wrapper Functions (Production Pattern)
# ---------------------------

def run_extract(**context):
    file_path = extract_data(
        api_url="https://fakestoreapi.com/products",
        execution_date=context["ds"],
    )
    return file_path 

def run_transform(**context):
    ti = context["ti"]

    file_path = ti.xcom_pull(
        task_ids="extract_and_upload_raw"
    )

    transform_and_load(file_path)


# ---------------------------
# DAG Definition
# ---------------------------

with DAG(
    dag_id="sales_pipeline_raw_ingestion",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    tags=["sales_pipeline", "raw"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_and_upload_raw",
        python_callable=run_extract,
        provide_context=True,
    )

    transform_task = PythonOperator(
        task_id="transform_and_load_products",
        python_callable=run_transform,
        provide_context=True,
    )

    extract_task >> transform_task
