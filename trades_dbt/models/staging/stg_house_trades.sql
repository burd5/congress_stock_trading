with house_trades as (
    select * from {{ source('postgres', 'house_trades') }}
),

remove_title as (
    select 
           id,
           CASE WHEN politician_name LIKE '%, Mr.. %' THEN 
                split_part(politician_name,  ', Mr.. ', 2) || ' ' || split_part(politician_name,  ', Mr.. ', 1)
                WHEN politician_name LIKE '%, Ms.. %' THEN 
                split_part(politician_name,  ', Ms.. ', 2) || ' ' || split_part(politician_name,  ', Ms.. ', 1)
                WHEN politician_name LIKE '%, Mrs.. %' THEN 
                split_part(politician_name,  ', Mrs.. ', 2) || ' ' || split_part(politician_name,  ', Mrs.. ', 1)
                WHEN politician_name LIKE '%, Hon.. %' THEN 
                split_part(politician_name,  ', Hon.. ', 2) || ' ' || split_part(politician_name,  ', Hon.. ', 1)
                WHEN politician_name LIKE '%,%' THEN 
                split_part(politician_name,  ', ', 2) || ' ' || split_part(politician_name,  ', ', 1)  
          ELSE politician_name
          END as politician_name
    from house_trades
),

first_and_last_only as (
    select id,
           split_part(politician_name, ' ', 1) || ' ' || split_part(politician_name, ' ', -1) as politician_name
    from remove_title
),

modify_purchased_or_sold as (
    select CASE WHEN purchased_or_sold = 'S' THEN 'Sale'
                WHEN purchased_or_sold = 'P' THEN 'Purchase'
                WHEN purchased_or_sold = 'E' THEN 'Exchange'
                WHEN purchased_or_sold = 'S (partial)' THEN 'Sale (partial)'
                END as purchased_or_sold
    from house_trades
)

select * from first_and_last_only