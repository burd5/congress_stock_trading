with senate_trades as (
    select * from {{ source('congress_trades', 'senate_trades') }}
),

politicians as (
    select * from {{ source('congress_trades', 'politicians') }}
),

convert_mixed_politician_names as (
    select
        CASE WHEN politician_name LIKE '%Ladda Duckworth%' THEN 'Tammy Duckworth'
             WHEN politician_name LIKE '%Rafael Cruz%' THEN 'Ted Cruz'
             WHEN politician_name LIKE '%Daniel Sullivan%' THEN 'Dan Sullivan'
             WHEN politician_name LIKE '%Debra Fischer%' THEN 'Deb Fischer'
             WHEN politician_name LIKE '%Chris Hollen%' THEN 'Chris Van Hollen'
             WHEN politician_name LIKE '%JD Vance%' THEN 'J.D. (James) Vance'
             WHEN politician_name LIKE '%Jeffry Flake%' THEN 'Jeff Flake'
             WHEN politician_name LIKE '%Jerry Moran,%' THEN 'Jerry Moran'
             WHEN politician_name LIKE '%Thomas Udall%' THEN 'Tom Udall'
             WHEN politician_name LIKE '%William IV%' THEN 'Bill Hagerty'
             WHEN politician_name LIKE '%Jefferson III%' THEN 'Jefferson Sessions'
             WHEN politician_name LIKE '%Joseph III%' THEN 'Joe Manchin'
             ELSE politician_name
        END AS politician_name,
        SPLIT_PART(stock_ticker, E'\n', 1) as stock_ticker,
        asset_name,
        purchased_or_sold,
        transaction_date,
        amount
    from senate_trades
),

asset_and_ticker_name_mod as (
    select
        cmn.politician_name as politician_name,
        p.id as politician_id,
        CASE WHEN length(stock_ticker) > 6 THEN '--' ELSE stock_ticker END AS stock_ticker,
        SPLIT_PART(asset_name, E'\n', 1) AS stock_information,
        purchased_or_sold,
        TO_DATE(transaction_date, 'MM-DD-YYYY') as transaction_date,
        amount
    from
        convert_mixed_politician_names cmn
    left join 
        politicians p
    on
        cmn.politician_name = p.name
)

select * from asset_and_ticker_name_mod