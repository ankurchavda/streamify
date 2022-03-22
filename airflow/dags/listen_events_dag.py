import os
from datetime import datetime

from airflow import DAG, macros
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator


GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
GCP_GCS_BUCKET = os.environ.get('GCP_GCS_BUCKET')
BIGQUERY_DATASET = os.environ.get('BIGQUERY_DATASET', 'streamify')
BIG_QUERY_TABLE_NAME = 'listen_events'

EXECUTION_MONTH = '{{ execution_date.strftime("%-m") }}'
EXECUTION_DAY = '{{ execution_date.strftime("%-d") }}'
EXECUTION_HOUR = '{{ execution_date.strftime("%-H") }}'
EXECUTION_DATETIME_STR = '{{ execution_date.strftime("%M%d%H") }}'

LISTEN_EVENTS_PATH = f'{BIG_QUERY_TABLE_NAME}/month={EXECUTION_MONTH}/day={EXECUTION_DAY}/hour={EXECUTION_HOUR}'

default_args = {
    'owner' : 'airflow'
}

with DAG(
    dag_id = 'listen_events_dag',
    default_args = default_args,
    description = 'Create external table for listen events data in BigQuery',
    schedule_interval="5 * * * *", #At the 5th minute of every hour
    start_date=datetime(2022,3,20),
    catchup=True,
    tags=['streamify']
) as dag:

    create_external_table_task = BigQueryCreateExternalTableOperator(
        task_id = 'create_external_table_task',
        table_resource = {
            'tableReference': {
            'projectId': GCP_PROJECT_ID,
            'datasetId': BIGQUERY_DATASET,
            'tableId': f'{BIG_QUERY_TABLE_NAME}_{EXECUTION_DATETIME_STR}',
            },
            'externalDataConfiguration': {
                'sourceFormat': 'PARQUET',
                'sourceUris': [f'gs://{GCP_GCS_BUCKET}/{LISTEN_EVENTS_PATH}/*'],
            },
        }
    )

    create_external_table_task