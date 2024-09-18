import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def obtener_esquema() -> str:
    """Obtiene el esquema de Redshift desde las variables de entorno."""
    esquema = os.getenv("REDSHIFT_SCHEMA", "public")
    return esquema

def obtener_credenciales() -> dict:
    """Recupera las credenciales de conexión a Redshift desde las variables de entorno."""
    credenciales = {
        "dbname": os.getenv("REDSHIFT_DB"),
        "user": os.getenv("REDSHIFT_USER"),
        "password": os.getenv("REDSHIFT_PWD"),
        "host": os.getenv("REDSHIFT_URL"),
        "port": os.getenv("REDSHIFT_PORT", 5439)
    }
    return credenciales

def argumentos_defecto_airflow():
    """Proporciona los argumentos por defecto para los DAGs de Airflow."""
    return {
        "owner": "ejmejias",
        "depends_on_past": False,
        "start_date": datetime.now(),
        "email_on_failure": True,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    }
