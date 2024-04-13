with merged_trades as (
    select * from {{ ref('stg_senate_trades') }}
    union
    select * from {{ ref('stg_house_trades') }}
),


politicians as (
    select * from {{ ref('stg_politicians') }} 
),

politician_info as (
    select mt.*,
           p.part_of_congress,
           p.political_party,
           p.office
    from merged_trades mt full outer join politicians p 
    on mt.politician_name = p.name
)

select * from politician_info