with politicians as (
    select * from {{ source('congress_trades', 'politicians') }}
)

select * from politicians