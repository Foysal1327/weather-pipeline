select
    dc.city_name,
    dc.country,
    fa.lead_time_hour_bucket,
    count(*)                                         as n_predictions,
    round(avg(fa.temperature_error_c)::numeric, 3)   as temperature_bias_c,
    round(avg(fa.temperature_abs_error_c)::numeric, 3) as temperature_mae_c,
    round(sqrt(avg(power(fa.temperature_error_c, 2)))::numeric, 3) as temperature_rmse_c,
    round(avg(fa.wind_abs_error_kmh)::numeric, 3)    as wind_mae_kmh,
    round(avg(fa.precipitation_brier_score)::numeric, 4) as precipitation_brier_score
from {{ ref('fact_forecast_accuracy') }} as fa
inner join {{ ref('dim_city') }} as dc
    on fa.city_key = dc.city_key
group by 1, 2, 3