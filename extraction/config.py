"""
Central config for the weather pipeline: cities and API settings.
Keep this as the single source of truth — extraction scripts and
(eventually) dbt seeds should reference this list, not hardcode cities.
"""

CITIES = [
    {"city_id": "dhaka",     "name": "Dhaka",     "country": "Bangladesh",    "latitude": 23.8103,  "longitude": 90.4125,   "timezone": "Asia/Dhaka"},
    {"city_id": "tokyo",     "name": "Tokyo",     "country": "Japan",         "latitude": 35.6762,  "longitude": 139.6503,  "timezone": "Asia/Tokyo"},
    {"city_id": "bangkok",   "name": "Bangkok",   "country": "Thailand",      "latitude": 13.7563,  "longitude": 100.5018,  "timezone": "Asia/Bangkok"},
    {"city_id": "sydney",    "name": "Sydney",    "country": "Australia",     "latitude": -33.8688, "longitude": 151.2093,  "timezone": "Australia/Sydney"},
    {"city_id": "new_york",  "name": "New York",  "country": "USA",           "latitude": 40.7128,  "longitude": -74.0060,  "timezone": "America/New_York"},
    {"city_id": "medina",    "name": "Medina",    "country": "Saudi Arabia",  "latitude": 24.5247,  "longitude": 39.5692,   "timezone": "Asia/Riyadh"},
]

# Open-Meteo endpoints
FORECAST_API_BASE = "https://api.open-meteo.com/v1/forecast"
ARCHIVE_API_BASE = "https://archive-api.open-meteo.com/v1/archive"

# Variables we pull — kept explicit (not "all") so raw schema stays predictable
CURRENT_VARS = ["temperature_2m", "relative_humidity_2m", "apparent_temperature",
                 "precipitation", "weather_code", "wind_speed_10m", "wind_direction_10m"]

HOURLY_FORECAST_VARS = ["temperature_2m", "relative_humidity_2m", "precipitation_probability",
                          "precipitation", "weather_code", "wind_speed_10m"]

HOURLY_HISTORICAL_VARS = ["temperature_2m", "relative_humidity_2m", "precipitation",
                            "weather_code", "wind_speed_10m"]