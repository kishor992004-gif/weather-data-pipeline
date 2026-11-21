select
    row_number() over (order by city) as city_key,
    city,
    max(latitude) as latitude,
    max(longitude) as longitude
from {{ source('staging', 'stg_weather_hourly') }}
group by city