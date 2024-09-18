import requests
import json
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Configuración de conexión a Redshift
api_key = os.getenv('FOOTBALL_API_KEY')
host = os.getenv('REDSHIFT_URL')
port = os.getenv('REDSHIFT_PORT')
dbname = os.getenv('REDSHIFT_DB')
user = os.getenv('REDSHIFT_USER')
password = os.getenv('REDSHIFT_PWD')

# Paso 1: Extrayendo Datos desde la API
url = 'https://api.football-data.org/v2/competitions/PL/matches'
headers = {'X-Auth-Token': api_key}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
else:
    print("Error fetching data from API")
    data = {}

# Paso 2: Transformación de Datos con Pandas
matches = data.get('matches', [])
df = pd.json_normalize(matches)

# Limpieza de datos
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)

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
    conn = None

# Función para cargar los datos
def cargar_en_redshift(conn, table_name, dataframe):
    if conn is None:
        print("No connection to Redshift.")
        return

    dtypes = dataframe.dtypes
    cols = list(dtypes.index)
    tipos = list(dtypes.values)
    type_map = {'int64': 'INT', 'float64': 'FLOAT', 'object': 'VARCHAR(255)'}
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
cargar_en_redshift(conn=conn, table_name='football_matches', dataframe=df)

if conn:
    conn.close()
