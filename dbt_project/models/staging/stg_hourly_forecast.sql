with source as (
    select * from {{ source('raw', 'hourly_forecast') }}
),

renamed as (
    select
        city_id,
        forecast_for,
        fetched_at,
        utc_offset_seconds,
        temperature_2m               as temperature_c,
        relative_humidity_2m         as relative_humidity_pct,
        precipitation_probability    as precipitation_probability_pct,
        precipitation                as precipitation_mm,
        weather_code,
        wind_speed_10m                as wind_speed_kmh,

        -- lead time: how far ahead of the forecast this prediction was made.
        -- this is the foundation of the forecast-accuracy-by-lead-time analysis.
        extract(epoch from (forecast_for - fetched_at)) / 3600.0 as lead_time_hours
    from source
)

select
    renamed.*,
    wmo.description as weather_description
from renamed
left join {{ ref('wmo_weather_codes') }} as wmo
    on renamed.weather_code = wmo.weather_code