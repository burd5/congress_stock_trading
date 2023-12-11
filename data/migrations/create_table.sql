DROP TABLE IF EXISTS congress_stock_transactions;

CREATE TABLE IF NOT EXISTS congress_stock_transactions(
    id serial primary key,
    name varchar(255),
    office varchar(255),
    filing_year varchar(255),
    asset_name varchar(255),
    transaction_type varchar(255),
    date_transacted date,
    date_notified date,
    amount varchar(255)
)