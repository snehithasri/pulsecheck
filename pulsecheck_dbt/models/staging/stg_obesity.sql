with source as (
    select * from {{ source('raw_data', 'RAW_OBESITY') }}
),

cleaned as (
    select
        yearstart::integer       as year_start,
        yearend::integer         as year_end,
        locationabbr             as state_code,
        locationdesc             as state_name,
        question                 as health_question,
        data_value::float        as data_value,
        data_value_type          as value_type,
        stratificationcategory1  as category,
        stratification1          as stratification,
        age_years                as age_group,
        race_ethnicity           as race_ethnicity,
        sex                      as gender
    from source
    where data_value is not null
)

select * from cleaned