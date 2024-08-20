import requests
import pandas as pd
from sqlalchemy import create_engine

# Paso 1: Extrayendo de Datos desde la API
url = 'https://api.football-data.org/v2/competitions/PL/matches'
response = requests.get(url)
data = response.json()

# Paso 2: Transformación de Datos con Pandas
df = pd.json_normalize(data)
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)
df['main.temp'] = df['main.temp'].astype(float)

# Paso 3: Cargando de Datos en Amazon Redshift
# Configurando la conexión a Redshift
engine = create_engine('postgresql+psycopg2://ejmejiasf_coderhouse:pAjkuk033c@redshift-cluster-https://api.football-data.org/v2/competitions/PL/matches')

# Carga los datos en Redshift
df.to_sql('mi tabla', engine, if_exists='replace', index=False)