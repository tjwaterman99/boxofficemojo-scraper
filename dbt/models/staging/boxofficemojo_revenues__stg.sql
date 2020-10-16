{{
    config(materialized="table")
}}

select
    revenues.data ->> '$.date' as date,
    revenues.data ->> '$.release' as title,
    revenues.data ->> '$.daily' as revenue,
    revenues.data ->> '$.theaters' as theaters,
    revenues.data ->> '$.distributor' as distributor
from {{ source('boxofficemojo', 'boxofficemojo_revenues') }} as revenues