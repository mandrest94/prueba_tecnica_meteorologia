import json
import logging
from datetime import datetime
from pathlib import Path

import requests
import yaml


# ---------------------------------------------------------
# Configuración de logs
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Rutas
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_FILE = BASE_DIR / "config" / "cities.yaml"
RAW_DIR = BASE_DIR / "data" / "raw"

API_URL = "https://archive-api.open-meteo.com/v1/archive"


# ---------------------------------------------------------
# Cargar configuración
# ---------------------------------------------------------

def load_config():
    """Carga ciudades, periodo y zona horaria desde YAML."""

    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config


# ---------------------------------------------------------
# Construir parámetros de Open-Meteo
# ---------------------------------------------------------

def build_params(city, config):
    """Construye dinámicamente los parámetros de consulta."""

    return {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "start_date": config["period"]["start_date"],
        "end_date": config["period"]["end_date"],
        "daily": ",".join([
            "temperature_2m_mean",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "rain_sum",
            "precipitation_hours",
            "wind_speed_10m_max",
        ]),
        "timezone": config["timezone"],
    }


# ---------------------------------------------------------
# Consulta API
# ---------------------------------------------------------

def fetch_weather(city, config):
    """Consulta Open-Meteo para una ciudad."""

    params = build_params(city, config)

    logger.info(
        "Consultando Open-Meteo para %s",
        city["name"]
    )

    response = requests.get(
        API_URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    return response.json()


# ---------------------------------------------------------
# Guardar RAW
# ---------------------------------------------------------

def save_raw(city, data):
    """Guarda la respuesta original de la API."""

    RAW_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    extraction_timestamp = datetime.now().strftime(
        "%Y%m%d"
    )

    filename = (
        f"{city['name'].lower()}_"
        f"{extraction_timestamp}.json"
    )

    output_file = RAW_DIR / filename

    raw_record = {
        "extraction_timestamp": datetime.now().isoformat(),
        "city": city["name"],
        "department": city["department"],
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "data": data,
    }

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            raw_record,
            file,
            ensure_ascii=False,
            indent=2
        )

    logger.info(
        "RAW guardado: %s",
        output_file
    )


# ---------------------------------------------------------
# Proceso principal
# ---------------------------------------------------------

def main():

    logger.info("Iniciando extracción meteorológica")

    config = load_config()

    cities = config["cities"]

    for city in cities:

        try:

            data = fetch_weather(
                city,
                config
            )

            save_raw(
                city,
                data
            )

        except requests.RequestException as error:

            logger.error(
                "Error consultando %s: %s",
                city["name"],
                error
            )

        except Exception as error:

            logger.exception(
                "Error procesando %s: %s",
                city["name"],
                error
            )

    logger.info("Extracción finalizada")


if __name__ == "__main__":
    main()