--create schema
CREATE SCHEMA IF NOT EXISTS sfc;
--create tables
CREATE TABLE IF NOT EXISTS sfc.stock(
    stock_code VARCHAR(50) NOT NULL,
    stock_name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT (now() at time zone 'utc'),
    updated_at TIMESTAMP NOT NULL DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY (stock_code)
);
CREATE TABLE IF NOT EXISTS sfc.short_positions(
    date DATE NOT NULL,
    stock_code VARCHAR(50) NOT NULL,
    shares NUMERIC(50,5) NOT NULL CHECK (shares >=0),
    hk_dollars NUMERIC(50,5) NOT NULL CHECK (hk_dollars >=0),
    created_at TIMESTAMP NOT NULL DEFAULT (now() at time zone 'utc'),
    updated_at TIMESTAMP NOT NULL DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY (date, stock_code),
    CONSTRAINT fk_stock_code FOREIGN KEY(stock_code) REFERENCES sfc.stock(stock_code) ON DELETE CASCADE
);
