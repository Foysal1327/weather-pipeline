"""
Thin wrapper around the Open-Meteo API. Keeps HTTP concerns (retries,
timeouts, error handling) in one place so extract_*.py scripts stay
focused on *what* to fetch, not *how*.
"""
import time
import requests

from extraction.config import FORECAST_API_BASE, ARCHIVE_API_BASE


class OpenMeteoClient:
    def __init__(self, timeout: int = 10, max_retries: int = 3, backoff_seconds: float = 1.5):
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_seconds = backoff_seconds
        self.session = requests.Session()

    def _get(self, url: str, params: dict) -> dict:
        last_exc = None
        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.session.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as exc:
                last_exc = exc
                if attempt < self.max_retries:
                    time.sleep(self.backoff_seconds * attempt)  # simple linear backoff
        raise RuntimeError(f"Failed after {self.max_retries} attempts: {last_exc}") from last_exc

    def get_current_and_forecast(self, latitude: float, longitude: float,
                                   current_vars: list[str], hourly_vars: list[str],
                                   timezone: str = "auto", forecast_days: int = 3) -> dict:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ",".join(current_vars),
            "hourly": ",".join(hourly_vars),
            "timezone": timezone,
            "forecast_days": forecast_days,
        }
        return self._get(FORECAST_API_BASE, params)

    def get_historical(self, latitude: float, longitude: float,
                         start_date: str, end_date: str,
                         hourly_vars: list[str], timezone: str = "auto") -> dict:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,   # "YYYY-MM-DD"
            "end_date": end_date,
            "hourly": ",".join(hourly_vars),
            "timezone": timezone,
        }
        return self._get(ARCHIVE_API_BASE, params)