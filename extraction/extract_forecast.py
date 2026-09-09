from datetime import datetime, timezone

from extraction.client import OpenMeteoClient
from extraction.config import CITIES, CURRENT_VARS, HOURLY_FORECAST_VARS
from extraction.db import save_hourly_forecast

def extract_hourly_forecast() -> list[dict]:
    client = OpenMeteoClient()
    records = []
    fetched_at = datetime.now(timezone.utc).isoformat()

    for city in CITIES:
        response = client.get_current_and_forecast(
            latitude=city["latitude"],
            longitude=city["longitude"],
            current_vars=CURRENT_VARS,
            hourly_vars=HOURLY_FORECAST_VARS,
            timezone=city["timezone"],
        )
        hourly = response["hourly"]
        utc_offset_seconds = response.get("utc_offset_seconds")
        times = hourly["time"]

        for i, forecast_time in enumerate(times):
            record = {
                "city_id": city["city_id"],
                "forecast_for": forecast_time,     # the hour this prediction is FOR
                "fetched_at": fetched_at,           # when this batch was pulled (= "lead time" anchor)
                "utc_offset_seconds": utc_offset_seconds,
                "temperature_2m": hourly["temperature_2m"][i],
                "relative_humidity_2m": hourly["relative_humidity_2m"][i],
                "precipitation_probability": hourly["precipitation_probability"][i],
                "precipitation": hourly["precipitation"][i],
                "weather_code": hourly["weather_code"][i],
                "wind_speed_10m": hourly["wind_speed_10m"][i],
            }
            records.append(record)

    return records


if __name__ == "__main__":
    results = extract_hourly_forecast()
    print(f"Extracted {len(results)} hourly forecast records")
    print(results[0])
    save_hourly_forecast(results)