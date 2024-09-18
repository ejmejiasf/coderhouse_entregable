import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
from .utils import get_credentials, get_schema

def create_table_if_not_exists(conn):
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {get_schema()}.football_matches (
        match_id INTEGER PRIMARY KEY,
        season_start_year INTEGER,
        season_end_year INTEGER,
        utc_date TIMESTAMP,
        status VARCHAR(50),
        home_team VARCHAR(100),
        away_team VARCHAR(100),
        home_score INTEGER,
        away_score INTEGER,
        competition VARCHAR(100)
    );
    """
    with conn.cursor() as cur:
        cur.execute(create_table_query)
        conn.commit()
    print(f"Table {get_schema()}.football_matches is ready.")

def cargar_data(exec_date, path):
    print(f"Cargando la data para la fecha: {exec_date}")
    date = datetime.strptime(exec_date, "%Y-%m-%d %H")
    csv_path = (
        f"{path}/processed_data/data_{date.year}-{date.month}-{date.day}-{date.hour}.csv"
    )

    records = pd.read_csv(csv_path, sep=",").fillna(0)

    print(records.shape)
    print(records.head())

    credentials = get_credentials()
    print(credentials)
    conn = psycopg2.connect(**credentials)
    create_table_if_not_exists(conn)
    
    columns = [
        "match_id",
        "season_start_year",
        "season_end_year",
        "utc_date",
        "status",
        "home_team",
        "away_team",
        "home_score",
        "away_score",
        "competition"
    ]
    
    cur = conn.cursor()
    table_name = "football_matches"
    
    values = [tuple(x) for x in records.to_numpy()]
    insert_sql = f"INSERT INTO {get_schema()}.{table_name} ({', '.join(columns)}) VALUES %s"
    
    cur.execute("BEGIN")
    execute_values(cur, insert_sql, values)
    cur.execute("COMMIT")

