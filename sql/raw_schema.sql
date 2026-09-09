CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.current_conditions (
    id                      BIGSERIAL PRIMARY KEY,
    city_id                 TEXT NOT NULL,
    observed_at             TIMESTAMP NOT NULL,      -- local time, per city timezone
    extracted_at            TIMESTAMPTZ NOT NULL,    -- when the pipeline pulled this
    utc_offset_seconds      INTEGER,
    temperature_2m          NUMERIC,
    relative_humidity_2m    NUMERIC,
    apparent_temperature    NUMERIC,
    precipitation           NUMERIC,
    weather_code            INTEGER,
    wind_speed_10m          NUMERIC,
    wind_direction_10m      NUMERIC,
    loaded_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (city_id, observed_at)
);

CREATE TABLE IF NOT EXISTS raw.hourly_forecast (
    id                          BIGSERIAL PRIMARY KEY,
    city_id                     TEXT NOT NULL,
    forecast_for                TIMESTAMP NOT NULL,   -- the future hour being predicted
    fetched_at                  TIMESTAMPTZ NOT NULL, -- when this prediction was made
    utc_offset_seconds          INTEGER,
    temperature_2m              NUMERIC,
    relative_humidity_2m        NUMERIC,
    precipitation_probability   NUMERIC,
    precipitation                NUMERIC,
    weather_code                INTEGER,
    wind_speed_10m               NUMERIC,
    loaded_at                    TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (city_id, forecast_for, fetched_at)
);

CREATE TABLE IF NOT EXISTS raw.historical (
    id                      BIGSERIAL PRIMARY KEY,
    city_id                 TEXT NOT NULL,
    observed_at             TIMESTAMP NOT NULL,
    fetched_at              TIMESTAMPTZ NOT NULL,
    utc_offset_seconds      INTEGER,
    temperature_2m          NUMERIC,
    relative_humidity_2m    NUMERIC,
    precipitation           NUMERIC,
    weather_code            INTEGER,
    wind_speed_10m          NUMERIC,
    loaded_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (city_id, observed_at)
);

-- indexes for the queries (dbt) will run most often:
-- filtering/joining by city and time range.
CREATE INDEX IF NOT EXISTS idx_current_conditions_city_time ON raw.current_conditions (city_id, observed_at);
CREATE INDEX IF NOT EXISTS idx_hourly_forecast_city_target ON raw.hourly_forecast (city_id, forecast_for);
CREATE INDEX IF NOT EXISTS idx_hourly_forecast_fetched_at ON raw.hourly_forecast (fetched_at);
CREATE INDEX IF NOT EXISTS idx_historical_city_time ON raw.historical (city_id, observed_at);