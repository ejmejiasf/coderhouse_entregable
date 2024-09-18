import json
import requests
from datetime import datetime

#Extraccion de datos
def extraer_data(exec_date, path):
    date = datetime.strptime(exec_date, "%Y-%m-%d %H")
    json_path = (
        f"{path}/raw_data/data_{date.year}-{date.month}-{date.day}-{date.hour}.json"
    )
    url = 'https://api.football-data.org/v2/competitions/PL/matches'
    headers = {'X-Auth-Token': '66f79342272442de8b7847f3e111e12b'}  # Reemplaza 'YOUR_API_KEY' con tu clave real

    try:
        print(f"Adquiriendo data para la fecha: {exec_date}")
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print("Success!")
            data = response.json()
            with open(
                json_path,
                "w",
            ) as json_file:
                json.dump(data, json_file)
            print("JSON File stored")
        else:
            print(f"An error has occurred. Status Code: {response.status_code}")
    except ValueError as e:
        print("Formato datetime debería ser %Y-%m-%d %H", e)
        raise e
