"""
Extracts current conditions for all configured cities and hands them
to the storage layer. Raw extraction stays "dumb": store what the API
gives us, decode/clean it later in dbt staging.
"""
from datetime import datetime, timezone

from extraction.client import OpenMeteoClient
from extraction.config import CITIES, CURRENT_VARS, HOURLY_FORECAST_VARS
from extraction.db import save_current_conditions

def extract_current_conditions() ->list[dict]:
    client = OpenMeteoClient()
    records = []
    for city in CITIES:
        response = client.get_current_and_forecast(
            latitude=city["latitude"],
            longitude=city["longitude"],
            current_vars=CURRENT_VARS,
            hourly_vars=HOURLY_FORECAST_VARS,
            timezone=city["timezone"],
        )
        current = response["current"]
        
        utc_offset_seconds = response.get("utc_offset_seconds")
        record = {
            "city_id": city["city_id"],
            "observed_at": current["time"],          # what moment this reading describes
            "extracted_at": datetime.now(timezone.utc).isoformat(),  # when we pulled it
            "utc_offset_seconds": utc_offset_seconds,
            "temperature_2m": current.get("temperature_2m"),
            "relative_humidity_2m": current.get("relative_humidity_2m"),
            "apparent_temperature": current.get("apparent_temperature"),
            "precipitation": current.get("precipitation"),
            "weather_code": current.get("weather_code"),
            "wind_speed_10m": current.get("wind_speed_10m"),
            "wind_direction_10m": current.get("wind_direction_10m"),
        }
        records.append(record)
    return records

if __name__ == "__main__":
    results = extract_current_conditions()
    for r in results:
        print(r)
    save_current_conditions(results)