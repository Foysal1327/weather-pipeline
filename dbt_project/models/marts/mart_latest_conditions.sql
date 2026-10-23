-- one row per city: the most recent current-conditions reading
with latest as (
    select distinct on (city_id) *
    from {{ ref('stg_current_conditions') }}
    order by city_id, extracted_at desc
)

select
    dc.city_key,
    dc.city_name,
    dc.country,
    dc.latitude,
    dc.longitude,
    latest.observed_at,
    latest.extracted_at,
    latest.temperature_c,
    latest.apparent_temperature_c,
    latest.relative_humidity_pct,
    latest.precipitation_mm,
    latest.weather_description,
    latest.wind_speed_kmh,
    latest.wind_direction_deg
from latest
inner join {{ ref('dim_city') }} as dc
    on latest.city_id = dc.city_id