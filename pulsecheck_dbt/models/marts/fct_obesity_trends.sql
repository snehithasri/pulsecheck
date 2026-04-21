with base as (
    select * from {{ ref('stg_obesity') }}
),

trends as (
    select
        year_start,
        state_code,
        state_name,
        health_question,
        category,
        stratification,
        gender,
        race_ethnicity,
        age_group,

        -- core metrics
        round(avg(data_value), 2)  as avg_prevalence,
        round(min(data_value), 2)  as min_prevalence,
        round(max(data_value), 2)  as max_prevalence,
        count(*)                   as record_count

    from base
    group by
        year_start, state_code, state_name,
        health_question, category, stratification,
        gender, race_ethnicity, age_group
)

select * from trends