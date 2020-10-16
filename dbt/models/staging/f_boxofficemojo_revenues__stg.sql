{{
    config(materialized="table")
}}

with extracted as (
    select
        revenues.data ->> 'date' as date,
        revenues.data ->> 'release' as title,
        revenues.data ->> 'daily' as revenue,
        revenues.data ->> 'theaters' as theaters,
        revenues.data ->> 'distributor' as distributor
    from {{ source('boxofficemojo', 'boxofficemojo_revenues') }} as revenues
)

, converted as (
    select
        md5(extracted.date || extracted.title)::uuid as id,
        extracted.date::date as date,
        extracted.title::varchar as title,
        replace(replace(extracted.revenue, '$', ''), ',', '')::integer as revenue,
        case 
            when extracted.theaters like '%-%' then null
            else replace(extracted.theaters, ',', '')::integer
        end as theaters,
        extracted.distributor::varchar as distributor
    from extracted
)

select * from converted