from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator

import requests
import json
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

def download_and_load_football_data():
    # Configuración de la API de fútbol
    api_key = '66f79342272442de8b7847f3e111e12b'
    url = 'https://api.football-data.org/v2/competitions/PL/matches'
    headers = {'X-Auth-Token': api_key}

    # Realizar la solicitud a la API
    response = requests.get(url, headers=headers)
    data_json = response.json()

    # Procesamiento de datos
    matches = data_json.get('matches', [])
    df = pd.json_normalize(matches)

    # Configuración de conexión a Redshift
    db_host = 'data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com'
    db_port = '5439'
    db_name = 'data-engineer-database'
    db_user = 'ejmejiasf_coderhouse'
    db_password = 'pAjkuk033c'

    try:
        conn = psycopg2.connect(
            host=db_host,
            dbname=db_name,
            user=db_user,
            password=db_password,
            port=db_port
        )
        print("Connected to Redshift successfully!")
    except Exception as e:
        print("Unable to connect to Redshift.")
        print(e)
        return

    # Función para cargar los datos en Redshift
    def cargar_en_redshift(conn, table_name, dataframe):
        dtypes = dataframe.dtypes
        cols = list(dtypes.index)
        tipos = list(dtypes.values)
        type_map = {'int64': 'INT', 'float64': 'FLOAT', 'object': 'VARCHAR(255)'}
        sql_dtypes = [type_map[str(dtype)] for dtype in tipos]
        column_defs = [f"{name} {data_type}" for name, data_type in zip(cols, sql_dtypes)]
        table_schema = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {', '.join(column_defs)}
            );
        """
        cur = conn.cursor()
        cur.execute(table_schema)
        values = [tuple(x) for x in dataframe.to_numpy()]
        insert_sql = f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES %s"
        cur.execute("BEGIN")
        execute_values(cur, insert_sql, values)
        cur.execute("COMMIT")
        print('Data loaded into Redshift successfully!')

    # Carga de datos en Redshift
    cargar_en_redshift(conn=conn, table_name='football_matches', dataframe=df)
    conn.close()

# Configuración del DAG y tareas
default_args = {
    'owner': 'ejmejiasf',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

api_dag = DAG(
    dag_id="football_data_pipeline",
    default_args=default_args,
    description="DAG para consumir API de fútbol y cargar datos en Redshift",
    start_date=datetime(2023, 5, 11, 2),
    schedule_interval='@daily'
)

task1 = BashOperator(
    task_id='start_task',
    bash_command='echo Iniciando...',
    dag=api_dag
)

task2 = PythonOperator(
    task_id='download_and_load_football_data',
    python_callable=download_and_load_football_data,
    dag=api_dag
)

task3 = BashOperator(
    task_id='end_task',
    bash_command='echo Proceso completado...',
    dag=api_dag
)

task1 >> task2 >> task3