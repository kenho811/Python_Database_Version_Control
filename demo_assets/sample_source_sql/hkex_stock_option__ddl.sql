-- create schema
CREATE SCHEMA IF NOT EXISTS hkex_stock_option;
-- create table
CREATE TABLE IF NOT EXISTS hkex_stock_option.stock(
    hkats_code VARCHAR(50) NOT NULL,
    sehk_code VARCHAR(50) NOT NULL,
    stock_name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT (now() at time zone 'utc'),
    updated_at TIMESTAMP NOT NULL DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY (hkats_code)
);
CREATE TABLE IF NOT EXISTS hkex_stock_option.stock_option(
    date DATE NOT NULL,
    hkats_code VARCHAR(50) NOT NULL,
    trading_volume_calls NUMERIC(50,5) NOT NULL CHECK (trading_volume_calls >=0),
    trading_volume_puts NUMERIC(50,5) NOT NULL CHECK (trading_volume_puts >=0),
    open_interest_calls NUMERIC(50,5) NOT NULL CHECK (open_interest_calls >=0),
    open_interest_puts NUMERIC(50,5) NOT NULL CHECK (open_interest_puts >=0),
    implied_volatility_decimal NUMERIC(5,3) NOT NULL CHECK (implied_volatility_decimal >=0),
    created_at TIMESTAMP NOT NULL DEFAULT (now() at time zone 'utc'),
    updated_at TIMESTAMP NOT NULL DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY (date, hkats_code),
    CONSTRAINT fk_stock_option FOREIGN KEY(hkats_code) REFERENCES hkex_stock_option.stock(hkats_code) ON DELETE CASCADE
);
