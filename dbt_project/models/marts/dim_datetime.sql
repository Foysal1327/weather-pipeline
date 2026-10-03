{% set start_date = "to_date('2026-01-01', 'YYYY-MM-DD')" %}
{% set end_date = "to_date('2027-12-31', 'YYYY-MM-DD')" %}

with spine as (
    {{ dbt_utils.date_spine(
        datepart="hour",
        start_date=start_date,
        end_date=end_date
    ) }}
),

renamed as (
    select
        date_hour as datetime_utc,
        cast(date_hour as date)              as date_day,
        extract(year from date_hour)          as year,
        extract(month from date_hour)         as month,
        extract(day from date_hour)           as day,
        extract(hour from date_hour)          as hour,
        extract(dow from date_hour)           as day_of_week,       -- 0=Sunday
        to_char(date_hour, 'Day')             as day_name,
        to_char(date_hour, 'Month')           as month_name,
        case when extract(dow from date_hour) in (0, 6)
             then true else false end         as is_weekend
    from spine
)


select
    -- surrogate key: one row per hour, used by fact tables to join
    {{ dbt_utils.generate_surrogate_key(['datetime_utc']) }} as datetime_key,
    *
from renamed