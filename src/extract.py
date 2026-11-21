import json
from datetime import date
from pathlib import Path

import requests

CITIES = {
    "Mumbai": (19.0760, 72.8777),
    "Delhi": (28.6139, 77.2090),
    "Bengaluru": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
}

URL = "https://api.open-meteo.com/v1/forecast"
RAW_DIR = Path("data/raw")


def fetch_city(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
        "past_days": 7,
        "forecast_days": 1,
        "timezone": "auto",
    }
    resp = requests.get(URL, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    for city, (lat, lon) in CITIES.items():
        data = fetch_city(lat, lon)
        out = RAW_DIR / f"weather_{city.lower()}_{today}.json"
        out.write_text(json.dumps(data))
        print(f"Saved {out}")


if __name__ == "__main__":
    main()