select
    c.city_key,
    cast(to_char(s.observed_at, 'YYYYMMDD') as int) as date_key,
    s.observed_at,
    s.temperature_c,
    s.humidity_pct,
    s.precipitation_mm,
    s.wind_speed_kmh
from {{ source('staging', 'stg_weather_hourly') }} s
join {{ ref('dim_city') }} c
    on s.city = c.city