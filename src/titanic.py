from airflow.operators.bash_operator import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from airflow import DAG

default_args= {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

with DAG(
    'titanic',
    default_args=default_args,
    description='ETL. Ingest: nifi. Transform: Spark. DW: Hive.'
    scheduler_interval='@daily',
    start_date=days_ago(1),
    tags=['edvai'],
) as dag: 

    comienza_proceso = EmptyOperator(
        task_id='start_task',
    )

    finaliza_proceso = EmptyOperator(
        task_id='end_task'
    )

    processing = BashOperator(
        task_id='ETL_Titanic_data'
        bash_command='ssh hadoop@172.17.0.2 /home/hadoop/spark/bin/spark-submit --files /home/hadoop/hive/conf/hive-site.xml /home/hadoop/airflow/dags/titanic.py '
    )

    comienza_proceso >> processing >> finaliza_proceso