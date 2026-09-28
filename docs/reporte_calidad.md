# Reporte de Calidad de Datos

## 1. Objetivo

Verificar la consistencia básica de los datos meteorológicos antes de su publicación en formato Parquet y su utilización en procesos analíticos.

## 2. Validaciones implementadas

El proceso de transformación ejecuta validaciones sobre los datos obtenidos desde la fuente histórica de Open-Meteo.

Las validaciones incluyen:

* Cantidad de registros.
* Fechas nulas.
* Valores nulos.
* Registros duplicados.
* Cantidad de ciudades.
* Fecha mínima.
* Fecha máxima.
* Consistencia de los datos por ciudad.

## 3. Resultado de las validaciones

Durante la ejecución del pipeline se obtuvo:

| Validación                            | Resultado               |
| ------------------------------------- | ----------------------- |
| Ciudades procesadas                   | 5                       |
| Periodo esperado                      | 01/01/2026 – 15/09/2026 |
| Registros por ciudad y archivo        | 258                     |
| Fechas nulas                          | 0                       |
| Valores nulos                         | 0                       |
| Duplicados dentro de cada archivo RAW | 0                       |
| Ciudades identificadas por archivo    | 1                       |
| Dataset mensual generado              | 45 registros            |

## 4. Control de duplicados

Durante la consolidación de los archivos RAW se identificaron registros repetidos entre diferentes ejecuciones de extracción.

Los archivos correspondientes a diferentes fechas de extracción contienen información histórica sobre el mismo periodo meteorológico. Por esta razón, una misma combinación de ciudad y fecha puede aparecer en más de un archivo RAW.

El proceso actualmente identifica estos registros y los reporta mediante logs.

Este comportamiento queda documentado como una oportunidad de mejora para una versión posterior del pipeline, donde se puede establecer explícitamente una llave de negocio:

`city + date`

para garantizar unicidad en el dataset diario consolidado.

## 5. Indicadores meteorológicos

El proceso genera indicadores derivados para facilitar el análisis:

* Día lluvioso.
* Lluvia intensa.
* Viento fuerte.
* Condición meteorológica adversa.

Los umbrales se encuentran definidos en la lógica de transformación.

## 6. Resultado final

El pipeline genera:

* Datos originales en la capa RAW.
* Dataset meteorológico diario procesado.
* Archivos Parquet particionados.
* Dataset mensual para consumo de BI.

Las pruebas automatizadas disponibles en el proyecto presentan actualmente:

**2 pruebas ejecutadas — 2 pruebas exitosas.**

## 7. Mejoras recomendadas

Para una implementación productiva se recomienda:

1. Implementar una llave única `city + date`.
2. Incorporar controles de calidad como tareas independientes dentro de Airflow.
3. Implementar métricas históricas de calidad.
4. Incorporar alertas ante fallos o cambios significativos en la calidad.
5. Incorporar validaciones de esquema antes de publicar los datos.
