with house_trades as (
    select * from {{ source('postgres', 'house_trades') }}
),

remove_title as (
    select 
           id,
           owner,
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
            CASE 
                WHEN SPLIT_PART(politician_name, ' ', 1) LIKE '%_.%' THEN SPLIT_PART(politician_name, ' ', 2) || ' ' || SPLIT_PART(politician_name, ' ', 3)
                ELSE split_part(politician_name, ' ', 1) || ' ' || split_part(politician_name, ' ', -1)
             END AS edited_politician_name
           
    from remove_title
),

edited_transaction_dates as (
    select id,
           SUBSTRING(transaction_date FROM '^\d{1,2}/\d{1,2}/\d{4}') as transaction_date
    from house_trades
),

edited_amounts as (
    select id,
           CASE 
                WHEN SPLIT_PART(amount, E'\n', 1) LIKE '%DC%' THEN SPLIT_PART(amount, E'\n', 2)
                WHEN SPLIT_PART(amount, E'\n', 1) IN ('$25,000,001 -', '$1,000,001 -', '$5,000,001 -') THEN SPLIT_PART(amount, E'\n', 1) || ' ' || SPLIT_PART(amount, E'\n', 2)
            ELSE
                SPLIT_PART(amount, E'\n', 1)
    END AS amount
    from house_trades
),

split_on_filing as (
    select id,
           SPLIT_PART(UPPER(stock_information), 'FILING', 1) as stock_information
    from house_trades
),

edited_stock_information as (
    select id,
           (REGEXP_MATCHES(stock_information, '\(([a-zA-Z]+)\)'))[1] as stock_ticker,
           SPLIT_PART(stock_information, E'\n', 1) || ' ' || SPLIT_PART(stock_information, E'\n', 2) as stock_information
    from split_on_filing
),

modify_purchased_or_sold as (
    select id,
           CASE WHEN purchased_or_sold = 'S' THEN 'Sale'
                WHEN purchased_or_sold = 'P' THEN 'Purchase'
                WHEN purchased_or_sold = 'E' THEN 'Exchange'
                WHEN purchased_or_sold = 'S (partial)' THEN 'Sale (partial)'
                END as purchased_or_sold
    from house_trades
),

combine_edited_columns as (
    select 
          mod.id as id,
          fl.edited_politician_name as politician_name,
          es.stock_ticker as stock_ticker,
          es.stock_information,
          mod.purchased_or_sold as purchased_or_sold,
          etd.transaction_date as transaction_date,
          ea.amount
    from first_and_last_only fl left join modify_purchased_or_sold mod
              on fl.id = mod.id left join house_trades 
              on house_trades.id = mod.id left join edited_transaction_dates etd
              on mod.id = etd.id left join edited_amounts ea 
              on etd.id = ea.id left join edited_stock_information es 
              on ea.id = es.id
)

select * from combine_edited_columns