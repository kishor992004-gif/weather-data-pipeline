import os

from sqlalchemy import create_engine, text

from transform import transform

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_URL = f"postgresql+psycopg2://de_user:de_pass@{DB_HOST}:5432/weather_dw"


def main():
    df = transform()
    engine = create_engine(DB_URL)
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS staging"))
    df.to_sql("stg_weather_hourly", engine, schema="staging",
              if_exists="replace", index=False)
    print(f"Loaded {len(df)} rows into staging.stg_weather_hourly")


if __name__ == "__main__":
    main()