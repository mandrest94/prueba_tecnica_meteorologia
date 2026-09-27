import pandas as pd

from src.transform import validate_dataframe


def test_validate_dataframe():

    df = pd.DataFrame({
        "city": [
            "Bogota",
            "Bogota"
        ],
        "date": pd.to_datetime([
            "2026-01-01",
            "2026-01-02"
        ]),
        "temperature_mean_c": [
            15.0,
            16.0
        ]
    })

    result = validate_dataframe(df)

    assert result["row_count"] == 2

    assert result["duplicates"] == 0

    assert result["null_dates"] == 0

    assert result["min_date"] == pd.Timestamp(
        "2026-01-01"
    )

    assert result["max_date"] == pd.Timestamp(
        "2026-01-02"
    )