# Prueba Técnica — Senior Data Engineering

Pipeline de datos meteorológicos históricos para cinco ciudades colombianas utilizando Open-Meteo, Python, Docker, Apache Parquet y Apache Airflow.

## 1. Descripción

El proyecto implementa un pipeline ETL para consultar información meteorológica histórica, transformarla y publicarla en formatos adecuados para análisis y visualización.

Ciudades procesadas:

* Bogotá
* Medellín
* Barranquilla
* Cali
* Villavicencio

Periodo:

**1 de enero de 2026 a 15 de septiembre de 2026**

Zona horaria:

`America/Bogota`

## 2. Arquitectura

```text
Open-Meteo
    │
    ▼
Extract
    │
    ▼
RAW JSON
    │
    ▼
Transform
    │
    ▼
Dataset diario
    │
    ├───────────────► Parquet particionado
    │
    ▼
Dataset mensual
    │
    ▼
BI / Visualización
```

La ejecución completa es orquestada mediante Apache Airflow.

## 3. Estructura del proyecto

```text
prueba_tecnica_meteorologia/
│
├── config/
│   └── cities.yaml
│
├── dags/
│   └── weather_pipeline.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── dashboard/
│
├── docs/
│   ├── diccionario_datos.md
│   └── reporte_calidad.md
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── __init__.py
│
├── tests/
│   ├── test_transform.py
│   └── test_validate.py
│
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md
```

## 4. Tecnologías

* Python 3.10
* Docker
* Docker Compose
* Apache Airflow 2.10.4
* Pandas
* PyArrow
* Apache Parquet
* Requests
* PyYAML
* Pytest

## 5. Fuente de datos

La información meteorológica se obtiene de la API histórica de Open-Meteo.

Endpoint:

`https://archive-api.open-meteo.com/v1/archive`

La configuración de las ciudades se encuentra en:

`config/cities.yaml`

Esto permite agregar o modificar ciudades sin modificar la lógica principal de extracción.

## 6. Capas de datos

### RAW

Las respuestas originales de la API se conservan en:

```text
data/raw/
```

Los archivos permiten identificar la ciudad y la fecha de extracción.

### Procesado

El dataset diario consolidado se genera en:

```text
data/processed/weather_daily.csv
```

### Parquet

Los datos procesados se almacenan en:

```text
data/processed/parquet/
```

utilizando particiones por:

```text
city/year/month
```

### Dashboard

El dataset resumido se genera en:

```text
data/dashboard/dashboard_weather_monthly.parquet
```

Contiene indicadores mensuales por ciudad.

## 7. Ejecución local

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar extracción:

```bash
python -m src.extract
```

Ejecutar transformación:

```bash
python -m src.transform
```

Ejecutar carga:

```bash
python -m src.load
```

## 8. Ejecución con Docker

Construir la imagen:

```bash
docker compose build
```

Ejecutar el pipeline:

```bash
docker compose up
```

El pipeline ejecuta:

```text
Extract → Transform → Load
```

Los datos se mantienen disponibles en la carpeta `data/` del proyecto mediante volúmenes Docker.

## 9. Airflow

Airflow se ejecuta mediante Docker.

Interfaz:

```text
http://localhost:8080
```

El DAG es:

```text
weather_pipeline
```

Flujo:

```text
extract_weather
        ↓
transform_weather
        ↓
load_parquet
```

El DAG está configurado para:

* Ejecución manual.
* `catchup=False`.
* Dos reintentos por tarea.
* Dependencias explícitas entre etapas.
* Registro de logs.

## 10. Pruebas

Las pruebas automatizadas se ejecutan mediante:

```bash
pytest
```

Resultado actual:

```text
2 passed
```

## 11. Calidad de datos

Se realizan controles sobre:

* Registros.
* Fechas.
* Valores nulos.
* Duplicados.
* Ciudades.
* Rango temporal.

Los resultados y oportunidades de mejora se encuentran documentados en:

```text
docs/reporte_calidad.md
```

## 12. Dataset para BI

El dataset mensual permite analizar:

* Comparación entre ciudades.
* Evolución mensual de temperatura.
* Temperatura máxima y mínima.
* Precipitación acumulada.
* Días lluviosos.
* Lluvia intensa.
* Viento fuerte.
* Condiciones adversas.

Visualizaciones propuestas:

1. Línea de temperatura promedio por ciudad.
2. Barras de precipitación mensual.
3. Comparación de días lluviosos por ciudad.
4. Indicadores KPI de temperatura y precipitación.
5. Tabla comparativa mensual.

## 13. Decisiones técnicas

### Python + Pandas

Se utiliza para simplificar la transformación de datos diarios y la generación de indicadores.

### Parquet

Se selecciona por ser un formato columnar adecuado para análisis y consumo de herramientas BI.

### Particionamiento

Se utiliza:

```text
city/year/month
```

para facilitar la lectura selectiva por ciudad y periodo.

### Docker

Permite reproducir el entorno y aislar las dependencias.

### Airflow

Permite orquestar las etapas del pipeline, controlar dependencias, reintentos y ejecución manual.

## 14. Limitaciones y mejoras futuras

La solución está diseñada para el alcance de una prueba técnica.

Para una implementación productiva se recomienda:

* Control de unicidad mediante `city + date`.
* Validaciones de calidad como tareas independientes.
* Alertas automáticas.
* Gestión de secretos.
* Monitoreo de ejecuciones.
* Data quality framework.
* Almacenamiento cloud.
* CI/CD.
* Mayor cobertura de pruebas.

## 15. Resultado

La solución permite ejecutar de forma reproducible el flujo:

```text
Open-Meteo
    ↓
Extract
    ↓
RAW
    ↓
Transform
    ↓
Dataset diario
    ↓
Parquet particionado
    ↓
Dataset mensual
    ↓
BI
```

y su ejecución puede ser orquestada mediante Apache Airflow.
