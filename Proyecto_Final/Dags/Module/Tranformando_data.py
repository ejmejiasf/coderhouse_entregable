import json
import pandas as pd
from datetime import datetime

def transformar_data(exec_date, path):
    print(f"Iniciando transformación de datos para: {exec_date}")

    # Formatear las rutas para los archivos JSON y CSV
    date = datetime.strptime(exec_date, "%Y-%m-%d %H")
    json_path = f"{path}/raw_data/data_{date.strftime('%Y-%m-%d-%H')}.json"
    csv_path = f"{path}/processed_data/data_{date.strftime('%Y-%m-%d-%H')}.csv"

    # Cargar datos desde el archivo JSON
    with open(json_path, "r") as file:
        data = json.load(file)

    # Procesar los datos de los partidos
    matches = data.get("matches", [])
    processed_data = []

    for match in matches:
        match_details = {
            "match_id": match.get("id"),
            "season_year": match.get("season", {}).get("startDate", "")[:4],
            "match_date": match.get("utcDate"),
            "status": match.get("status"),
            "home_team": match.get("homeTeam", {}).get("name"),
            "away_team": match.get("awayTeam", {}).get("name"),
            "home_score": match.get("score", {}).get("fullTime", {}).get("homeTeam"),
            "away_score": match.get("score", {}).get("fullTime", {}).get("awayTeam"),
            "competition_name": match.get("competition", {}).get("name")
        }
        processed_data.append(match_details)

    # Convertir la lista de diccionarios en un DataFrame de pandas
    df_matches = pd.DataFrame(processed_data)

    # Guardar el DataFrame en un archivo CSV
    df_matches.to_csv(csv_path, index=False)
    print(f"Datos transformados y guardados en: {csv_path}")
