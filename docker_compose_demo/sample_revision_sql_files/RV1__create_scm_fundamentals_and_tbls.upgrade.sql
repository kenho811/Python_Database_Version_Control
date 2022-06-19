-- create schema
CREATE SCHEMA IF NOT EXISTS fundamentals;
-- create table
CREATE TABLE IF NOT EXISTS fundamentals.source
  (
     source_id INTEGER PRIMARY KEY,
     source VARCHAR(50) NOT NULL UNIQUE,
     created_at TIMESTAMP NOT NULL DEFAULT (now() at time zone 'utc'),
     CONSTRAINT source_ux UNIQUE (source)
  );
-- Initialise with pre-set source
INSERT INTO fundamentals.source (source_id, source)
VALUES (1, 'yahoo'), (2, 'investing_dot_com') on conflict do nothing;
-- create table
CREATE TABLE IF NOT EXISTS fundamentals.price
  (
     ticker VARCHAR(10) NOT NULL,
     date DATE NOT NULL,
     open   NUMERIC(50,10) NOT NULL CHECK (open >=0),
     high   NUMERIC(50,10) NOT NULL CHECK (high >=0),
     low   NUMERIC(50,10) NOT NULL CHECK (low >=0),
     close   NUMERIC(50,10) NOT NULL CHECK (close >=0),
     adj_close   NUMERIC(50,10) NOT NULL CHECK (adj_close >=0),
     volume   NUMERIC(50,10) NOT NULL CHECK (volume >=0),
     source_id  INTEGER,
     created_at TIMESTAMP NOT NULL DEFAULT (now() at time zone 'utc'),
     updated_at TIMESTAMP NOT NULL DEFAULT (now() at time zone 'utc'),
     PRIMARY KEY (ticker, date),
     CONSTRAINT fk_source FOREIGN KEY(source_id) REFERENCES fundamentals.source(source_id) ON DELETE CASCADE
  );
