with stg as (
    select * from {{ ref('stg_hourly_forecast') }}
),

utc_normalized as (
    select
        city_id,
        forecast_for,                                    -- kept as-is: local time, for display
        fetched_at,
        utc_offset_seconds,

        -- convert the naive local timestamp to a true UTC instant by subtracting the offset
        (forecast_for - (utc_offset_seconds * interval '1 second'))
            at time zone 'UTC' as forecast_for_utc,

        temperature_c,
        relative_humidity_pct,
        precipitation_probability_pct,
        precipitation_mm,
        weather_code,
        weather_description,
        wind_speed_kmh
    from stg
),

with_lead_time as (
    select
        *,
        extract(epoch from (forecast_for_utc - fetched_at)) / 3600.0 as lead_time_hours
    from utc_normalized
)

select * from with_lead_time