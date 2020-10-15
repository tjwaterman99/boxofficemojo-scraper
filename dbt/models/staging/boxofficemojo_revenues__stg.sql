{{
    config(materialized="table")
}}

select *
from {{ source('boxofficemojo', 'boxofficemojo_revenues') }}