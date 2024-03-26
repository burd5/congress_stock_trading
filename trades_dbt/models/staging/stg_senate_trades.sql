with senate_trades as (
    select * from {{ source('postgres', 'senate_trades') }}
),

asset_and_ticker_name_mod as (
    select
        id,
        owner,
        politician_name,
        SPLIT_PART(stock_ticker, E'\n', 1) as stock_ticker,
        SPLIT_PART(asset_name, E'\n', 1) AS stock_information,
        purchased_or_sold,
        transaction_date,
        amount
    from
        senate_trades
)

select * from asset_and_ticker_name_mod