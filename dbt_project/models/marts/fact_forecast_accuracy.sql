with forecast as (
    select * from {{ ref('fact_forecast') }}
),

actuals as (
    select * from {{ ref('fact_historical_actuals') }}
),
joined as (
    select
        f.city_key,
        f.datetime_key,
        f.forecast_for_utc,
        f.fetched_at,
        f.lead_time_hours,

        f.temperature_c                       as predicted_temperature_c,
        a.temperature_c                       as actual_temperature_c,
        f.wind_speed_kmh                      as predicted_wind_speed_kmh,
        a.wind_speed_kmh                      as actual_wind_speed_kmh,
        f.precipitation_probability_pct,
        a.precipitation_mm                    as actual_precipitation_mm,
        f.weather_code                        as predicted_weather_code,
        a.weather_code                        as actual_weather_code,

        -- "did it actually rain this hour?" (0.1 mm is the usual wet-hour threshold)
        case when a.precipitation_mm >= 0.1 then 1 else 0 end as actual_rain_flag
    from forecast as f
    inner join actuals as a
        on f.city_key = a.city_key
        and f.datetime_key = a.datetime_key
)

select
    *,
    floor(lead_time_hours)::int                                  as lead_time_hour_bucket,
    predicted_temperature_c - actual_temperature_c               as temperature_error_c,
    abs(predicted_temperature_c - actual_temperature_c)          as temperature_abs_error_c,
    abs(predicted_wind_speed_kmh - actual_wind_speed_kmh)        as wind_abs_error_kmh,
    -- Brier score: squared gap between predicted rain probability and what happened (0 = perfect)
    power((precipitation_probability_pct / 100.0) - actual_rain_flag, 2) as precipitation_brier_score
from joined