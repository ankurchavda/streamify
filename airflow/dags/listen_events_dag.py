import os
import json
from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

from schema import schema
from bigquery_tasks import (create_external_table, 
                            create_empty_table, 
                            insert_job, 
                            delete_external_table)

BIG_QUERY_TABLE_NAME = 'listen_events'

GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
GCP_GCS_BUCKET = os.environ.get('GCP_GCS_BUCKET')
BIGQUERY_DATASET = os.environ.get('BIGQUERY_DATASET', 'streamify_stg')

EXECUTION_MONTH = '{{ logical_date.strftime("%-m") }}'
EXECUTION_DAY = '{{ logical_date.strftime("%-d") }}'
EXECUTION_HOUR = '{{ logical_date.strftime("%-H") }}'
EXECUTION_DATETIME_STR = '{{ logical_date.strftime("%m%d%H") }}'

EXTERNAL_TABLE_NAME = f'{BIG_QUERY_TABLE_NAME}_{EXECUTION_DATETIME_STR}'

EVENTS_PATH = f'{BIG_QUERY_TABLE_NAME}/month={EXECUTION_MONTH}/day={EXECUTION_DAY}/hour={EXECUTION_HOUR}'

EVENTS_SCHEMA = schema[BIG_QUERY_TABLE_NAME]

INSERT_QUERY = f"""
    INSERT `{BIGQUERY_DATASET}.{BIG_QUERY_TABLE_NAME}`
    SELECT * 
    FROM `{BIGQUERY_DATASET}.{EXTERNAL_TABLE_NAME}`
"""

default_args = {
    'owner' : 'airflow'
}

with DAG(
    dag_id = f'{BIG_QUERY_TABLE_NAME}_dag',
    default_args = default_args,
    description = f'Create external table for {BIG_QUERY_TABLE_NAME} data in BigQuery',
    schedule_interval="5 * * * *", #At the 5th minute of every hour
    start_date=datetime(2022,3,20),
    catchup=True,
    max_active_runs=3,
    tags=['streamify']
) as dag:

    create_external_table_task = create_external_table(GCP_PROJECT_ID, 
                                                       BIGQUERY_DATASET, 
                                                       EXTERNAL_TABLE_NAME, 
                                                       GCP_GCS_BUCKET, 
                                                       EVENTS_PATH)

    create_empty_table_task = create_empty_table(GCP_PROJECT_ID,
                                                 BIGQUERY_DATASET,
                                                 BIG_QUERY_TABLE_NAME,
                                                 EVENTS_SCHEMA)

    execute_insert_query_task = insert_job(INSERT_QUERY,
                                           BIGQUERY_DATASET,
                                           GCP_PROJECT_ID)


    delete_external_table_task = delete_external_table(GCP_PROJECT_ID, 
                                                       BIGQUERY_DATASET, 
                                                       EXTERNAL_TABLE_NAME)

    create_external_table_task >> create_empty_table_task >> execute_insert_query_task >> delete_external_table_task