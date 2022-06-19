create schema if not exists datetime;
create table if not exists datetime.special_date(
  date date primary key,
  is_hk_public_holiday boolean default False,
  created_at TIMESTAMP NOT NULL DEFAULT (now() at time zone 'utc'),
  updated_at TIMESTAMP NOT NULL DEFAULT (now() at time zone 'utc')
);