with house_trades as (
    select * from {{ source('congress_trades', 'house_trades') }}
),

politicians as (
    select * from {{ source('congress_trades', 'politicians') }}
),

remove_title as (
    select 
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
          END as politician_name,
          stock_information,
          purchased_or_sold,
          transaction_date,
          amount
    from house_trades
),

first_and_last_only as (
    select 
            CASE 
                WHEN SPLIT_PART(politician_name, ' ', 1) LIKE '%_.%' THEN SPLIT_PART(politician_name, ' ', 2) || ' ' || SPLIT_PART(politician_name, ' ', 3)
                ELSE split_part(politician_name, ' ', 1) || ' ' || split_part(politician_name, ' ', -1)
             END AS edited_politician_name,
             stock_information,
            purchased_or_sold,
            transaction_date,
            amount
    from remove_title
    where transaction_date != '' 
),

revise_edge_names as (
    select 
           CASE WHEN edited_politician_name LIKE '%Neal FACS%' THEN 'Richard Neal'
                ELSE edited_politician_name
            END AS politician_name,
           stock_information,
           purchased_or_sold,
           transaction_date,
           amount
    from first_and_last_only
),

edited_transaction_dates as (
    select 
          politician_name,
          stock_information,
          purchased_or_sold,
          SUBSTRING(transaction_date FROM '^\d{1,2}/\d{1,2}/\d{4}') as transaction_date,
          amount
    from revise_edge_names
    where TO_DATE(transaction_date, 'MM-DD-YYYY') <= CURRENT_DATE
),

edited_amounts as (
    select 
           politician_name,
           stock_information,
           purchased_or_sold,
           TO_DATE(transaction_date, 'MM-DD-YYYY') as transaction_date,
           CASE 
                WHEN SPLIT_PART(amount, E'\n', 1) IN ('$15,001 -', '$50,001 -', '$100,001 -', '$250,001 -', '$500,001 -', '$25,000,001 -', '$1,000,001 -', '$5,000,001 -') THEN SPLIT_PART(amount, E'\n', 1) || ' ' || SPLIT_PART(amount, E'\n', 2)
                WHEN SPLIT_PART(amount, E'\n', 1) LIKE '%DC%' THEN SPLIT_PART(amount, E'\n', 2)
            ELSE
                SPLIT_PART(amount, E'\n', 1)
    END AS amount
    from edited_transaction_dates
),

split_on_filing as (
    select 
           politician_name,
           SPLIT_PART(UPPER(stock_information), 'FILING', 1) as stock_information,
           purchased_or_sold,
           transaction_date,
           CASE WHEN amount LIKE'$1,001 -' THEN '$1,0001 - $5,000' ELSE amount END as amount
    from edited_amounts
),

edited_stock_information as (
    select 
           politician_name,
           CASE 
               WHEN POSITION('(' IN stock_information) > 0 AND POSITION(')' IN stock_information) > 0 THEN
                   SUBSTRING(stock_information, POSITION('(' IN stock_information) + 1, POSITION(')' IN stock_information) - POSITION('(' IN stock_information) - 1)
               ELSE '--' 
           END as stock_ticker,
           SPLIT_PART(stock_information, E'\n', 1) || ' ' || SPLIT_PART(stock_information, E'\n', 2) as stock_information,
           purchased_or_sold,
           transaction_date,
           amount
    from split_on_filing
),

modify_purchased_or_sold as (
    select 
           politician_name,
           p.id as politician_id,
           CASE WHEN length(stock_ticker) > 6 THEN '--' ELSE stock_ticker END AS stock_ticker,
           stock_information,
           CASE WHEN purchased_or_sold = 'S' THEN 'Sale'
                WHEN purchased_or_sold = 'P' THEN 'Purchase'
                WHEN purchased_or_sold = 'E' THEN 'Exchange'
                WHEN purchased_or_sold = 'S (partial)' THEN 'Sale (partial)'
                ELSE purchased_or_sold
                END as purchased_or_sold,
            transaction_date,
            amount
    from edited_stock_information esi
    left join 
        politicians p
    on
        esi.politician_name = p.name
)

select * from modify_purchased_or_sold