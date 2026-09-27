import json
import logging
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# Configuración
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


# ---------------------------------------------------------
# Umbrales meteorológicos
# ---------------------------------------------------------

RAIN_THRESHOLD_MM = 1.0
HEAVY_RAIN_THRESHOLD_MM = 20.0
STRONG_WIND_THRESHOLD_KMH = 40.0


# ---------------------------------------------------------
# Lectura RAW
# ---------------------------------------------------------

def read_raw_file(file_path):
    """Lee un archivo JSON de la capa RAW."""

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ---------------------------------------------------------
# Transformación de una ciudad
# ---------------------------------------------------------

def transform_city(raw_record):
    """Convierte el JSON RAW de una ciudad en DataFrame diario."""

    city = raw_record["city"]
    department = raw_record["department"]
    latitude = raw_record["latitude"]
    longitude = raw_record["longitude"]

    daily = raw_record["data"]["daily"]

    df = pd.DataFrame(daily)

    # -----------------------------------------------------
    # Renombrar columnas
    # -----------------------------------------------------

    df = df.rename(
        columns={
            "time": "date",
            "temperature_2m_mean": "temperature_mean_c",
            "temperature_2m_max": "temperature_max_c",
            "temperature_2m_min": "temperature_min_c",
            "precipitation_sum": "precipitation_mm",
            "rain_sum": "rain_mm",
            "precipitation_hours": "precipitation_hours",
            "wind_speed_10m_max": "wind_speed_max_kmh",
        }
    )

    # -----------------------------------------------------
    # Metadatos
    # -----------------------------------------------------

    df["city"] = city
    df["department"] = department
    df["latitude"] = latitude
    df["longitude"] = longitude

    # -----------------------------------------------------
    # Tipos
    # -----------------------------------------------------

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    numeric_columns = [
        "temperature_mean_c",
        "temperature_max_c",
        "temperature_min_c",
        "precipitation_mm",
        "rain_mm",
        "precipitation_hours",
        "wind_speed_max_kmh",
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # -----------------------------------------------------
    # Año y mes
    # -----------------------------------------------------

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    # -----------------------------------------------------
    # Indicadores meteorológicos
    # -----------------------------------------------------

    df["is_rainy_day"] = (
        df["precipitation_mm"] >= RAIN_THRESHOLD_MM
    )

    df["is_heavy_rain"] = (
        df["precipitation_mm"] >= HEAVY_RAIN_THRESHOLD_MM
    )

    df["is_strong_wind"] = (
        df["wind_speed_max_kmh"] >= STRONG_WIND_THRESHOLD_KMH
    )

    df["is_adverse_day"] = (
        df["is_heavy_rain"]
        | df["is_strong_wind"]
    )

    return df


# ---------------------------------------------------------
# Validaciones
# ---------------------------------------------------------

def validate_dataframe(df):
    """Ejecuta controles básicos de calidad."""

    validation_results = {}

    # Filas
    validation_results["row_count"] = len(df)

    # Duplicados
    validation_results["duplicates"] = int(
        df.duplicated(
            subset=["city", "date"]
        ).sum()
    )

    # Fechas nulas
    validation_results["null_dates"] = int(
        df["date"].isna().sum()
    )

    # Valores faltantes
    validation_results["null_values"] = int(
        df.isna().sum().sum()
    )

    # Fecha mínima
    validation_results["min_date"] = (
        df["date"].min()
    )

    # Fecha máxima
    validation_results["max_date"] = (
        df["date"].max()
    )

    return validation_results


# ---------------------------------------------------------
# Transformación completa
# ---------------------------------------------------------

def transform_all():

    logger.info(
        "Iniciando transformación de datos RAW"
    )

    all_dataframes = []

    raw_files = sorted(
        RAW_DIR.glob("*.json")
    )

    if not raw_files:

        raise FileNotFoundError(
            "No se encontraron archivos RAW."
        )

    for raw_file in raw_files:

        logger.info(
            "Procesando: %s",
            raw_file.name
        )

        raw_record = read_raw_file(
            raw_file
        )

        df_city = transform_city(
            raw_record
        )

        validation = validate_dataframe(
            df_city
        )

        logger.info(
            "Validación %s: %s",
            raw_record["city"],
            validation
        )

        all_dataframes.append(
            df_city
        )

    final_df = pd.concat(
        all_dataframes,
        ignore_index=True
    )

    # -----------------------------------------------------
    # Control global de duplicados
    # -----------------------------------------------------

    duplicates = final_df.duplicated(
        subset=["city", "date"]
    ).sum()

    if duplicates > 0:

        logger.warning(
            "Se encontraron %s duplicados.",
            duplicates
        )

        final_df = final_df.drop_duplicates(
            subset=["city", "date"]
        )

    # -----------------------------------------------------
    # Crear directorio de salida
    # -----------------------------------------------------

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        PROCESSED_DIR /
        "weather_daily.csv"
    )

    final_df.to_csv(
        output_file,
        index=False
    )

    logger.info(
        "Datos transformados guardados en: %s",
        output_file
    )

    logger.info(
        "Total registros: %s",
        len(final_df)
    )

    return final_df


if __name__ == "__main__":

    transform_all()