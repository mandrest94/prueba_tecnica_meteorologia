from pathlib import Path
import argparse

import pandas as pd
import matplotlib.pyplot as plt


def load_dataset(path: str) -> pd.DataFrame:
    """Carga el dataset mensual preparado para BI."""
    df = pd.read_parquet(path)

    required = {
        "city",
        "year",
        "month",
        "temperature_avg",
        "temperature_max",
        "temperature_min",
        "rainy_days",
        "heavy_rain_days",
        "strong_wind_days",
        "adverse_days",
    }

    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"Faltan columnas requeridas en el dataset BI: {sorted(missing)}"
        )

    # El nombre puede variar según la versión de load.py.
    if "precipitation_total_mm" in df.columns:
        precipitation_col = "precipitation_total_mm"
    elif "precipitation_total" in df.columns:
        precipitation_col = "precipitation_total"
    else:
        raise ValueError(
            "No se encontró la columna de precipitación "
            "('precipitation_total_mm' o 'precipitation_total')."
        )

    df["period"] = pd.to_datetime(
        df["year"].astype(str) + "-" + df["month"].astype(str) + "-01"
    )

    return df.sort_values(["city", "period"]), precipitation_col


def save_temperature_trend(df: pd.DataFrame, output_dir: Path) -> None:
    plt.figure(figsize=(11, 6))

    for city, data in df.groupby("city"):
        plt.plot(
            data["period"],
            data["temperature_avg"],
            marker="o",
            label=city,
        )

    plt.title("Temperatura promedio mensual por ciudad")
    plt.xlabel("Mes")
    plt.ylabel("Temperatura promedio (°C)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "01_temperatura_promedio.png", dpi=150)
    plt.close()


def save_precipitation(df: pd.DataFrame, precipitation_col: str, output_dir: Path) -> None:
    summary = (
        df.groupby("city", as_index=False)[precipitation_col]
        .sum()
        .sort_values(precipitation_col, ascending=False)
    )

    plt.figure(figsize=(10, 6))
    plt.bar(summary["city"], summary[precipitation_col])

    plt.title("Precipitación acumulada por ciudad")
    plt.xlabel("Ciudad")
    plt.ylabel("Precipitación acumulada (mm)")
    plt.xticks(rotation=20)
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "02_precipitacion_acumulada.png", dpi=150)
    plt.close()


def save_adverse_days(df: pd.DataFrame, output_dir: Path) -> None:
    summary = (
        df.groupby("city", as_index=False)["adverse_days"]
        .sum()
        .sort_values("adverse_days", ascending=False)
    )

    plt.figure(figsize=(10, 6))
    plt.bar(summary["city"], summary["adverse_days"])

    plt.title("Días con condiciones meteorológicas adversas")
    plt.xlabel("Ciudad")
    plt.ylabel("Número de días")
    plt.xticks(rotation=20)
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "03_dias_adversos.png", dpi=150)
    plt.close()


def save_weather_indicators(df: pd.DataFrame, output_dir: Path) -> None:
    summary = (
        df.groupby("city", as_index=False)[
            ["rainy_days", "heavy_rain_days", "strong_wind_days"]
        ]
        .sum()
        .sort_values("rainy_days", ascending=False)
    )

    x = range(len(summary))
    width = 0.25

    plt.figure(figsize=(11, 6))
    plt.bar(
        [i - width for i in x],
        summary["rainy_days"],
        width=width,
        label="Días lluviosos",
    )
    plt.bar(
        x,
        summary["heavy_rain_days"],
        width=width,
        label="Lluvia fuerte",
    )
    plt.bar(
        [i + width for i in x],
        summary["strong_wind_days"],
        width=width,
        label="Viento fuerte",
    )

    plt.title("Indicadores meteorológicos por ciudad")
    plt.xlabel("Ciudad")
    plt.ylabel("Número de días")
    plt.xticks(list(x), summary["city"], rotation=20)
    plt.grid(axis="y", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "04_indicadores_meteorologicos.png", dpi=150)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Visualización del dataset meteorológico preparado para BI."
    )
    parser.add_argument(
        "--input",
        default="data/dashboard/dashboard_weather_monthly.parquet",
        help="Ruta del dataset Parquet de BI.",
    )
    parser.add_argument(
        "--output",
        default="data/dashboard/visualizaciones",
        help="Directorio donde se guardarán las gráficas.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(
            f"No existe el dataset BI: {input_path}"
        )

    output_dir.mkdir(parents=True, exist_ok=True)

    df, precipitation_col = load_dataset(str(input_path))

    print("Dataset BI cargado correctamente")
    print(f"Registros: {len(df)}")
    print(f"Ciudades: {df['city'].nunique()}")
    print(
        f"Periodo: {df['period'].min():%Y-%m} "
        f"a {df['period'].max():%Y-%m}"
    )

    save_temperature_trend(df, output_dir)
    save_precipitation(df, precipitation_col, output_dir)
    save_adverse_days(df, output_dir)
    save_weather_indicators(df, output_dir)

    print(f"Visualizaciones generadas en: {output_dir}")


if __name__ == "__main__":
    main()
