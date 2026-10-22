with historical as (
    select * from {{ ref('int_historical_utc') }}
),

joined as (
    select
        dc.city_key,
        dd.datetime_key,
        historical.observed_at,
        historical.observed_at_utc,
        historical.temperature_c,
        historical.relative_humidity_pct,
        historical.precipitation_mm,
        historical.weather_code,
        historical.weather_description,
        historical.wind_speed_kmh
    from historical
    inner join {{ ref('dim_city') }} as dc
        on historical.city_id = dc.city_id
    inner join {{ ref('dim_datetime') }} as dd
        on historical.observed_at_utc = dd.datetime_utc
)

select * from joined