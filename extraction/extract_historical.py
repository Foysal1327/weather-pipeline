from datetime import datetime, timedelta, timezone

from extraction.client import OpenMeteoClient
from extraction.config import CITIES, HOURLY_HISTORICAL_VARS
from extraction.db import save_historical

def extract_historical_for_range(start_date: str, end_date: str) -> list[dict]:
    client = OpenMeteoClient()
    records = []
    fetched_at = datetime.now(timezone.utc).isoformat()

    for city in CITIES:
        response = client.get_historical(
            latitude=city["latitude"],
            longitude=city["longitude"],
            start_date=start_date,
            end_date=end_date,
            hourly_vars=HOURLY_HISTORICAL_VARS,
            timezone=city["timezone"],
        )
        hourly = response["hourly"]
        utc_offset_seconds = response.get("utc_offset_seconds")
        times = hourly["time"]

        for i, observed_time in enumerate(times):
            record = {
                "city_id": city["city_id"],
                "observed_at": observed_time,
                "fetched_at": fetched_at,
                "utc_offset_seconds": utc_offset_seconds,
                "temperature_2m": hourly["temperature_2m"][i],
                "relative_humidity_2m": hourly["relative_humidity_2m"][i],
                "precipitation": hourly["precipitation"][i],
                "weather_code": hourly["weather_code"][i],
                "wind_speed_10m": hourly["wind_speed_10m"][i],
            }
            records.append(record)

    return records

def backfill_historical(days_back: int = 30) -> list[dict]:
    end = datetime.now(timezone.utc).date() - timedelta(days=2)  # respect the lag
    start = end - timedelta(days=days_back)
    return extract_historical_for_range(start.isoformat(), end.isoformat())

if __name__ == "__main__":
    results = backfill_historical(days_back=30)
    print(f"Extracted {len(results)} historical records")
    print(results[0])
    save_historical(results)