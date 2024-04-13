with stocks as (
    select * from {{ source('congress_trades', 'stocks') }}
)

select * from stocks