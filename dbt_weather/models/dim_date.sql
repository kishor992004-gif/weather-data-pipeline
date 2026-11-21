select distinct
    cast(to_char(observed_at, 'YYYYMMDD') as int) as date_key,
    cast(observed_at as date) as full_date,
    cast(extract(year from observed_at) as int) as year,
    cast(extract(month from observed_at) as int) as month,
    cast(extract(day from observed_at) as int) as day,
    trim(to_char(observed_at, 'Day')) as day_name
from {{ source('staging', 'stg_weather_hourly') }}