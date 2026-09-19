with source as (
    select * from {{ source('raw', 'historical') }}
),

renamed as (
    select
        city_id,
        observed_at,
        fetched_at,
        utc_offset_seconds,
        temperature_2m          as temperature_c,
        relative_humidity_2m    as relative_humidity_pct,
        precipitation            as precipitation_mm,
        weather_code,
        wind_speed_10m            as wind_speed_kmh
    from source
)

select
    renamed.*,
    wmo.description as weather_description
from renamed
left join {{ ref('wmo_weather_codes') }} as wmo
    on renamed.weather_code = wmo.weather_code