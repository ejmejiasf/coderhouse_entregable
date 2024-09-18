-- Crear un esquema para organizar las tablas relacionadas con datos de fútbol
CREATE SCHEMA IF NOT EXISTS ejmejiasf_coderhouse;

-- Crear una tabla para almacenar información sobre los partidos de fútbol
CREATE TABLE ejmejiasf_coderhouse.match_details (
    id SERIAL PRIMARY KEY,  -- Identificador único para cada entrada
    partido_id INTEGER NOT NULL,  -- ID del partido proporcionado por la API
    temporada VARCHAR(9) NOT NULL,  -- Año de inicio y fin de la temporada en formato "YYYY-YYYY"
    fecha_partido TIMESTAMP NOT NULL,  -- Fecha y hora del partido
    estado_partido VARCHAR(50),  -- Estado actual del partido (ej. programado, finalizado)
    nombre_equipo_local VARCHAR(150),  -- Nombre del equipo que juega en casa
    nombre_equipo_visitante VARCHAR(150),  -- Nombre del equipo visitante
    puntaje_equipo_local SMALLINT,  -- Puntaje final del equipo local
    puntaje_equipo_visitante SMALLINT,  -- Puntaje final del equipo visitante
    nombre_competencia VARCHAR(150)  -- Nombre de la competencia o liga
);
