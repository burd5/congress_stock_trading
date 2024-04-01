DROP TABLE IF EXISTS house_trades;
DROP TABLE IF EXISTS senate_trades;
DROP TABLE IF EXISTS report_links;

CREATE TABLE IF NOT EXISTS house_trades(
    id serial primary key,
    owner varchar(255),
    politician_name varchar(255),
    stock_information varchar(255),
    purchased_or_sold varchar(255),
    transaction_date varchar(255),
    report_date varchar(255),
    amount varchar(255)
);

CREATE TABLE IF NOT EXISTS senate_trades(
    id serial primary key,
    politician_name varchar(255),
    transaction_date varchar(255),
    owner varchar(255),
    stock_ticker varchar(255),
    asset_name varchar(255),
    asset_type varchar(255),
    purchased_or_sold varchar(255),
    amount varchar(255),
    comment varchar(2000)
);

CREATE TABLE IF NOT EXISTS report_links(
    id serial primary key,
    link varchar(255)
);

