# Diccionario de Datos — Pipeline Meteorológico

## Dataset diario

Archivo principal:

`data/processed/weather_daily.csv`

Los datos diarios contienen información meteorológica histórica de cinco ciudades colombianas para el periodo comprendido entre el 1 de enero de 2026 y el 15 de septiembre de 2026.

| Campo                | Tipo              | Descripción                                                                  |
| -------------------- | ----------------- | ---------------------------------------------------------------------------- |
| `date`               | date              | Fecha de observación meteorológica.                                          |
| `city`               | string            | Ciudad donde se realizó la observación.                                      |
| `department`         | string            | Departamento al que pertenece la ciudad.                                     |
| `latitude`           | float             | Latitud geográfica de la ciudad.                                             |
| `longitude`          | float             | Longitud geográfica de la ciudad.                                            |
| `year`               | integer           | Año correspondiente a la fecha de observación.                               |
| `month`              | integer           | Mes correspondiente a la fecha de observación.                               |
| `temperature_mean_c` | float             | Temperatura media diaria en grados Celsius.                                  |
| `temperature_max_c`  | float             | Temperatura máxima diaria en grados Celsius.                                 |
| `temperature_min_c`  | float             | Temperatura mínima diaria en grados Celsius.                                 |
| `precipitation_mm`   | float             | Precipitación acumulada durante el día, expresada en milímetros.             |
| `wind_max_kmh`       | float             | Velocidad máxima del viento durante el día, expresada en km/h.               |
| `is_rainy_day`       | integer / boolean | Indicador de día lluvioso según el umbral definido en la transformación.     |
| `is_heavy_rain`      | integer / boolean | Indicador de lluvia intensa según el umbral definido en la transformación.   |
| `is_strong_wind`     | integer / boolean | Indicador de viento fuerte según el umbral definido en la transformación.    |
| `is_adverse_day`     | integer / boolean | Indicador de condiciones meteorológicas adversas según las reglas definidas. |

## Dataset mensual para BI

Archivo:

`data/dashboard/dashboard_weather_monthly.parquet`

Este dataset resume la información diaria por ciudad, departamento, año y mes.

| Campo                    | Tipo    | Descripción                                             |
| ------------------------ | ------- | ------------------------------------------------------- |
| `city`                   | string  | Ciudad.                                                 |
| `department`             | string  | Departamento.                                           |
| `year`                   | integer | Año.                                                    |
| `month`                  | integer | Mes.                                                    |
| `temperature_avg`        | float   | Temperatura promedio mensual.                           |
| `temperature_max`        | float   | Temperatura máxima registrada durante el mes.           |
| `temperature_min`        | float   | Temperatura mínima registrada durante el mes.           |
| `precipitation_total_mm` | float   | Precipitación acumulada durante el mes.                 |
| `rainy_days`             | integer | Número de días lluviosos durante el mes.                |
| `heavy_rain_days`        | integer | Número de días con lluvia intensa.                      |
| `strong_wind_days`       | integer | Número de días con viento fuerte.                       |
| `adverse_days`           | integer | Número de días con condiciones meteorológicas adversas. |

## Particionamiento

Los datos meteorológicos procesados se almacenan en formato Apache Parquet utilizando particiones por:

* `city`
* `year`
* `month`

Esta estructura facilita la consulta y lectura selectiva de información por ciudad y periodo.

## Métricas disponibles

El dataset permite analizar:

* Evolución mensual de temperatura.
* Temperatura promedio, máxima y mínima.
* Precipitación acumulada.
* Cantidad de días lluviosos.
* Cantidad de días con lluvia intensa.
* Cantidad de días con viento fuerte.
* Cantidad de días con condiciones adversas.
* Comparación meteorológica entre ciudades.
