-- DROP DATABASE IF EXISTS football_analysis;

-- CREATE DATABASE football_analysis;

-- Crear un esquema para organizar tus tablas
CREATE SCHEMA IF NOT EXISTS soccer_data_schema;

-- Crear la tabla para almacenar datos de los partidos
CREATE TABLE soccer_data_schema.match_details (
    id SERIAL PRIMARY KEY,
    match_id INTEGER NOT NULL,
    season_year VARCHAR(9) NOT NULL,  -- Combina año de inicio y fin
    match_date TIMESTAMP NOT NULL,
    match_status VARCHAR(50),
    home_team_name VARCHAR(150),
    away_team_name VARCHAR(150),
    home_team_score SMALLINT,
    away_team_score SMALLINT,
    competition_name VARCHAR(150)
);
