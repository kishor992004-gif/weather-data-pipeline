import json
from datetime import date
from pathlib import Path

import pandas as pd

RAW_DIR = Path("data/raw")


def transform(run_date=None):
    run_date = run_date or date.today().isoformat()
    frames = []
    for f in RAW_DIR.glob(f"weather_*_{run_date}.json"):
        data = json.loads(f.read_text())
        df = pd.DataFrame(data["hourly"])
        df["city"] = f.stem.split("_")[1].title()
        df["latitude"] = data["latitude"]
        df["longitude"] = data["longitude"]
        frames.append(df)

    if not frames:
        raise FileNotFoundError(f"No raw files found for {run_date}. Run extract.py first.")

    df = pd.concat(frames, ignore_index=True)
    df = df.rename(columns={
        "time": "observed_at",
        "temperature_2m": "temperature_c",
        "relative_humidity_2m": "humidity_pct",
        "precipitation": "precipitation_mm",
        "wind_speed_10m": "wind_speed_kmh",
    })
    df["observed_at"] = pd.to_datetime(df["observed_at"])
    df = df.drop_duplicates(subset=["city", "observed_at"])
    df = df.dropna(subset=["temperature_c"])
    df["ingested_at"] = pd.Timestamp.now()
    return df


if __name__ == "__main__":
    out = transform()
    print(out.head())
    print(out.shape)