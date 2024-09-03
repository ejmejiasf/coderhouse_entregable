import requests
import json
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Paso 1: Extrayendo de Datos desde la API
url = 'https://api.football-data.org/v2/competitions/PL/matches'
api_key = '66f79342272442de8b7847f3e111e12b'
response = requests.get(url)
data = response.json()

# Paso 2: Transformación de Datos con Pandas
df = pd.json_normalize(data)
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)
df['main.temp'] = df['main.temp'].astype(float)

# Configuración de conexión a Redshift
host = 'data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com'
dbname = 'data-engineer-database'
port = '5439'
user = 'ejmejiasf_coderhouse'
password = 'pAjkuk033c'

try:
    conn = psycopg2.connect(
        host=host,
        dbname=dbname,
        user=user,
        password=password,
        port=port
    )
    print("Connected to Redshift successfully!")
except Exception as e:
    print("Unable to connect to Redshift.")
    print(e)

# Función para cargar los datos
def cargar_en_redshift(conn, table_name, dataframe):
    dtypes = dataframe.dtypes
    cols = list(dtypes.index)
    tipos = list(dtypes.values)
    type_map = {'int64': 'INT', 'float64': 'FLOAT', 'object': 'VARCHAR(50)'}
    sql_dtypes = [type_map[str(dtype)] for dtype in tipos]
    
    # Definir formato SQL VARIABLE TIPO_DATO
    column_defs = [f"{name} {data_type}" for name, data_type in zip(cols, sql_dtypes)]
    
    # Crear la tabla si no existe
    table_schema = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {', '.join(column_defs)}
        );
    """
    
    # Crear la tabla
    cur = conn.cursor()
    cur.execute(table_schema)
    
    # Generar los valores a insertar
    values = [tuple(x) for x in dataframe.to_numpy()]
    
    # Definir el INSERT
    insert_sql = f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES %s"
    
    # Insertar los datos
    cur.execute("BEGIN")
    execute_values(cur, insert_sql, values)
    cur.execute("COMMIT")
    print('Proceso terminado')
    cur.close()

# Carga de datos en RedShift
cargar_en_redshift(conn=conn, table_name='mi_tabla', dataframe=df)

conn.close()
