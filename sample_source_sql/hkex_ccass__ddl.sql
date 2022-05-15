CREATE SCHEMA IF NOT EXISTS hkex_ccass;
-- Create table for market roles
CREATE TABLE IF NOT EXISTS hkex_ccass.market_role
(  role_id   integer,
   role_name   VARCHAR(100) NOT NULL,
   created_at TIMESTAMP NOT NULL DEFAULT (now() at time zone 'utc'),
   updated_at TIMESTAMP NOT NULL DEFAULT (now() at time zone 'utc'),
   PRIMARY KEY (role_id)
);
-- Initialise it with pre-set roles
INSERT INTO hkex_ccass.market_role (role_id, role_name)
VALUES (1, 'Retail Investor'), (2, 'Market Maker'), (3, 'American Investor'), (4, 'European Investor'), (5, 'Mainland China Investor'), (6, 'Market Intermediaries') on conflict do nothing;
-- Create participant table
CREATE TABLE IF NOT EXISTS hkex_ccass.participant
(  participant_id   VARCHAR(50) NOT NULL,
   participant_name   VARCHAR(100) NOT NULL,
   custom_participant_name   VARCHAR(100) DEFAULT NULL,
   role_id  integer NOT NULL DEFAULT 1,
   created_at TIMESTAMP NOT NULL DEFAULT (now() at time zone 'utc'),
   updated_at TIMESTAMP NOT NULL DEFAULT (now() at time zone 'utc'),
   PRIMARY KEY (participant_id),
   CONSTRAINT fk_market_role FOREIGN KEY(role_id) REFERENCES hkex_ccass.market_role(role_id) ON DELETE CASCADE
);
-- Create stock table
CREATE TABLE IF NOT EXISTS hkex_ccass.stock
(
  stock_code   VARCHAR(50) NOT NULL,
  stock_name   VARCHAR(100) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT (now() at time zone 'utc'),
  updated_at TIMESTAMP NOT NULL DEFAULT (now() at time zone 'utc'),
  PRIMARY KEY (stock_code)
);
-- Create participant_stock_shareholding table
CREATE TABLE IF NOT EXISTS hkex_ccass.participant_stock_shareholding
  (  stock_code   VARCHAR(50) NOT NULL,
     participant_id   VARCHAR(50) NOT NULL,
     date DATE NOT NULL,
     shareholding_amount  NUMERIC(50,5) NOT NULL CHECK (shareholding_amount >=0),
     shareholding_decimal   NUMERIC(50,10) NOT NULL CHECK (shareholding_decimal >=0 AND shareholding_decimal <=1),
     created_at TIMESTAMP NOT NULL DEFAULT (now() at time zone 'utc'),
     updated_at TIMESTAMP NOT NULL DEFAULT (now() at time zone 'utc'),
     PRIMARY KEY (stock_code, participant_id, date),
     CONSTRAINT fk_stock_code FOREIGN KEY(stock_code) REFERENCES hkex_ccass.stock(stock_code) ON DELETE CASCADE,
     CONSTRAINT fk_participant_id FOREIGN KEY(participant_id) REFERENCES hkex_ccass.participant(participant_id) ON DELETE CASCADE
  );
-- Update the market roles of those participants
-- Set Market Maker
UPDATE hkex_ccass.participant
SET role_id = 2
WHERE participant_id in ('C00019', 'B01654');
-- Set American Investor
UPDATE hkex_ccass.participant
SET role_id = 3
WHERE participant_id in ('C00100', 'C00010', 'B01274', 'B01451', 'B01224');
-- Set European Investor
UPDATE hkex_ccass.participant
SET role_id = 4
WHERE participant_id in ('B01161', 'C00093', 'C00074', 'B01121', 'B01491');
-- Set Mainland China Investor. ALl Mainland China investors' participant id start with 'A'.
UPDATE hkex_ccass.participant
SET role_id = 5
WHERE participant_id like 'A%';
-- Set Market Intermediaries
UPDATE hkex_ccass.participant
SET role_id = 6
WHERE participant_id in ('市場中介者');
