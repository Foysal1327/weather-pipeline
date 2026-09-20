with stg as (
    select * from {{ ref('stg_historical') }}
),

utc_normalized as (
    select
        city_id,
        observed_at,                                     -- local time, for display
        fetched_at,
        utc_offset_seconds,

        (observed_at - (utc_offset_seconds * interval '1 second'))
            at time zone 'UTC' as observed_at_utc,

        temperature_c,
        relative_humidity_pct,
        precipitation_mm,
        weather_code,
        weather_description,
        wind_speed_kmh
    from stg
)

select * from utc_normalized