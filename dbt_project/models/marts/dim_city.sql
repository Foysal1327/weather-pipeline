with cities as (
    select * from {{ ref('cities') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['city_id']) }} as city_key,
    city_id,
    city_name,
    country,
    latitude,
    longitude,
    timezone
from cities