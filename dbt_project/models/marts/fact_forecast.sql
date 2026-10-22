with forecast as (
    select * from {{ ref('int_hourly_forecast_utc') }}
    where lead_time_hours >= 0   -- exclude past/current hours bundled in the API response; see int_hourly_forecast_utc.sql docs
),

joined as (
    select
        dc.city_key,
        dd.datetime_key,
        forecast.forecast_for,
        forecast.forecast_for_utc,
        forecast.fetched_at,
        forecast.lead_time_hours,
        forecast.temperature_c,
        forecast.relative_humidity_pct,
        forecast.precipitation_probability_pct,
        forecast.precipitation_mm,
        forecast.weather_code,
        forecast.weather_description,
        forecast.wind_speed_kmh
    from forecast
    inner join {{ ref('dim_city') }} as dc
        on forecast.city_id = dc.city_id
    inner join {{ ref('dim_datetime') }} as dd
        on forecast.forecast_for_utc = dd.datetime_utc
)

select * from joined