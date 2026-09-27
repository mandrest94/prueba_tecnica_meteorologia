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

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "weather_daily.csv"
)

PARQUET_DIR = (
    BASE_DIR
    / "data"
    / "processed"
    / "parquet"
)

DASHBOARD_DIR = (
    BASE_DIR
    / "data"
    / "dashboard"
)


# ---------------------------------------------------------
# Cargar datos
# ---------------------------------------------------------

def load_data():

    if not INPUT_FILE.exists():

        raise FileNotFoundError(
            f"No existe el archivo: {INPUT_FILE}"
        )

    logger.info(
        "Leyendo datos procesados..."
    )

    df = pd.read_csv(
        INPUT_FILE,
        parse_dates=["date"]
    )

    return df


# ---------------------------------------------------------
# Guardar Parquet particionado
# ---------------------------------------------------------

def save_partitioned_parquet(df):

    PARQUET_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    logger.info(
        "Generando Parquet particionado..."
    )

    df.to_parquet(
        PARQUET_DIR,
        engine="pyarrow",
        partition_cols=[
            "city",
            "year",
            "month"
        ],
        index=False
    )

    logger.info(
        "Parquet generado en: %s",
        PARQUET_DIR
    )


# ---------------------------------------------------------
# Dataset mensual para BI
# ---------------------------------------------------------

def generate_dashboard_dataset(df):

    logger.info(
        "Generando dataset mensual para dashboard..."
    )

    dashboard_df = (
        df
        .groupby(
            [
                "city",
                "department",
                "year",
                "month"
            ],
            as_index=False
        )
        .agg(
            temperature_avg=(
                "temperature_mean_c",
                "mean"
            ),
            temperature_max=(
                "temperature_max_c",
                "max"
            ),
            temperature_min=(
                "temperature_min_c",
                "min"
            ),
            precipitation_total_mm=(
                "precipitation_mm",
                "sum"
            ),
            rainy_days=(
                "is_rainy_day",
                "sum"
            ),
            heavy_rain_days=(
                "is_heavy_rain",
                "sum"
            ),
            strong_wind_days=(
                "is_strong_wind",
                "sum"
            ),
            adverse_days=(
                "is_adverse_day",
                "sum"
            )
        )
    )

    DASHBOARD_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        DASHBOARD_DIR
        / "dashboard_weather_monthly.parquet"
    )

    dashboard_df.to_parquet(
        output_file,
        engine="pyarrow",
        index=False
    )

    logger.info(
        "Dataset para dashboard generado: %s",
        output_file
    )

    logger.info(
        "Registros mensuales: %s",
        len(dashboard_df)
    )

    return dashboard_df


# ---------------------------------------------------------
# Proceso principal
# ---------------------------------------------------------

def main():

    logger.info(
        "Iniciando carga analítica"
    )

    df = load_data()

    save_partitioned_parquet(df)

    dashboard_df = generate_dashboard_dataset(
        df
    )

    logger.info(
        "Proceso de carga finalizado"
    )

    return dashboard_df


if __name__ == "__main__":

    main()