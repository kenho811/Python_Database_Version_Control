-- Create schema
create schema if not exists hkex_index_future;
-- Create table
create table if not exists hkex_index_future.index(
  index_id varchar(20) primary key,
  index_name varchar(50) NOT NULL,
  created_at timestamp not null default (now() at time zone 'utc'),
  updated_at timestamp not null default (now() at time zone 'utc')
);
-- Initialise table
INSERT INTO hkex_index_future.index(index_id, index_name)
VALUES ('HSI', 'Hang Seng Index') on conflict do nothing;
-- Create table
create table if not exists hkex_index_future.future(
  future_id varchar(20) primary key,
  future_name varchar(50) NOT NULL,
  created_at timestamp not null default (now() at time zone 'utc'),
  updated_at timestamp not null default (now() at time zone 'utc')
);
-- Initialise table
INSERT INTO hkex_index_future.future(future_id, future_name)
VALUES ('HSIF', 'Hang Seng Index Future') on conflict do nothing;
-- Create table
create table if not exists hkex_index_future.source(
  source_id integer primary key,
  source_name varchar(50) NOT NULL,
  created_at timestamp not null default (now() at time zone 'utc'),
  updated_at timestamp not null default (now() at time zone 'utc')
);
-- Initialise table
INSERT INTO hkex_index_future.source(source_id, source_name)
VALUES (1, 'Quandl'), (2, 'InvestingDotCom'), (3, 'EtNet') on conflict do nothing;
-- Create table
create table if not exists hkex_index_future.index_future(
  index_id varchar(20) NOT NULL,
  future_id varchar(20) NOT NULL,
  source_id integer NOT NULL,
  date date NOT NULL,
  high  NUMERIC(50,5) NOT NULL CHECK (high >=0),
  low   NUMERIC(50,5) NOT NULL CHECK (low >=0),
  open   NUMERIC(50,5) NOT NULL CHECK (open >=0),
  close   NUMERIC(50,5) NOT NULL CHECK (close >=0),
  volume   NUMERIC(50,5) NOT NULL CHECK (volume >=0),
  created_at timestamp not null default (now() at time zone 'utc'),
  updated_at timestamp not null default (now() at time zone 'utc'),
  PRIMARY KEY (index_id, future_id, source_id, date),
  CONSTRAINT fk_index_id FOREIGN KEY(index_id) REFERENCES hkex_index_future.index(index_id) ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_source_id FOREIGN KEY(source_id) REFERENCES hkex_index_future.source(source_id) ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_future_id FOREIGN KEY(future_id) REFERENCES hkex_index_future.future(future_id) ON UPDATE CASCADE ON DELETE RESTRICT
);
