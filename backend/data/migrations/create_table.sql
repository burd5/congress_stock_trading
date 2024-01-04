DROP TABLE IF EXISTS trades;
DROP TABLE IF EXISTS politicians;
DROP TABLE IF EXISTS stocks;

CREATE TABLE IF NOT EXISTS trades(
    id serial primary key,
    stock_id integer,
    politician_id integer,
    purchased_or_sold varchar(255),
    transaction_date date,
    amount varchar(255)
);

CREATE TABLE IF NOT EXISTS politicians(
    id serial primary key,
    name varchar(255),
    part_of_congress varchar(255),
    state varchar(255),
    political_party varchar(255),
    office varchar(255)
);

CREATE TABLE IF NOT EXISTS stocks(
    id serial primary key,
    stock_marker VARCHAR(255) UNIQUE,
    company_name VARCHAR(255)
);

\copy stocks (stock_marker, company_name) FROM 'combined_stocks.csv' DELIMITER ',' CSV HEADER;

\copy politicians (name, part_of_congress, state, political_party, office) FROM 'current_leg.csv' DELIMITER ',' CSV HEADER;

\copy politicians (name, part_of_congress, state, political_party, office) FROM 'historical_leg.csv' DELIMITER ',' CSV HEADER;