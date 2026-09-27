import pandas as pd

from src.transform import transform_city


def test_transform_city():

    raw_record = {
        "city": "Bogota",
        "department": "Cundinamarca",
        "latitude": 4.7110,
        "longitude": -74.0721,
        "data": {
            "daily": {
                "time": [
                    "2026-01-01",
                    "2026-01-02"
                ],
                "temperature_2m_mean": [
                    14.5,
                    15.0
                ],
                "temperature_2m_max": [
                    20.0,
                    21.0
                ],
                "temperature_2m_min": [
                    9.0,
                    10.0
                ],
                "precipitation_sum": [
                    5.0,
                    25.0
                ],
                "rain_sum": [
                    5.0,
                    25.0
                ],
                "precipitation_hours": [
                    3.0,
                    8.0
                ],
                "wind_speed_10m_max": [
                    20.0,
                    45.0
                ]
            }
        }
    }

    df = transform_city(raw_record)

    assert len(df) == 2

    assert df["city"].iloc[0] == "Bogota"

    assert pd.api.types.is_datetime64_any_dtype(
        df["date"]
    )

    assert "year" in df.columns
    assert "month" in df.columns

    assert "is_rainy_day" in df.columns
    assert "is_heavy_rain" in df.columns
    assert "is_strong_wind" in df.columns
    assert "is_adverse_day" in df.columns