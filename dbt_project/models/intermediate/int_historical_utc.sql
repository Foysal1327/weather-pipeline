with stg as (
    select * from {{ ref('stg_historical') }}
),

cities as (
    select city_id, timezone as city_timezone from {{ ref('cities') }}
),

utc_normalized as (
    select
        stg.city_id,
        stg.observed_at,                                   -- local time, for display
        stg.fetched_at,
        stg.utc_offset_seconds,                            -- kept for audit only, no longer used in math

        -- interpret the naive local timestamp in the city's own timezone (DST-aware)
        stg.observed_at at time zone cities.city_timezone as observed_at_utc,

        stg.temperature_c,
        stg.relative_humidity_pct,
        stg.precipitation_mm,
        stg.weather_code,
        stg.weather_description,
        stg.wind_speed_kmh
    from stg
    inner join cities on stg.city_id = cities.city_id
)

select *
from utc_normalized
where observed_at_utc at time zone (select city_timezone from cities where cities.city_id = utc_normalized.city_id) = observed_at