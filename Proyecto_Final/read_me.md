# Proyecto Final

Este es un proyecto ETL desarrollado en Apache Airflow que extrae datos de la API de Football Data, los transforma y los carga en un Data Warehouse.

## Estructura del Proyecto

- `Dags/`: Contiene los DAGs de Airflow.
- `Modules/`: Contiene los módulos Python para extracción, transformación, carga y envío de correos.
- `.env`: Archivo para almacenar credenciales sensibles (no incluido en el repositorio).
- `.gitignore`: Lista de archivos y carpetas a ignorar por Git.
- `README.md`: Documentación del proyecto.

## Configuración

1. Crea un archivo `.env` en el directorio raíz con las credenciales necesarias.
2. Instala las dependencias utilizando `pip install -r requirements.txt`.

## Ejecución

1. Inicia Airflow utilizando Docker o una instalación local.
2. Asegúrate de que los DAGs estén habilitados en la interfaz web de Airflow.
3. Monitorea la ejecución y verifica los resultados en el Data Warehouse.

## Notas

- Asegúrate de tener configurado correctamente el acceso a la API y al Data Warehouse.
- Revisa las configuraciones SMTP para el envío de correos electrónicos.
