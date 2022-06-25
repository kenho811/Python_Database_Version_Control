create or replace view datetime.vw_trading_days_since_2021 as with weekdays (weekday) as (
select
	dt
-- Set timezone of now() to UTC
from
	generate_series('2021-01-01':: date, now() at time zone 'utc', '1 day':: interval) dt
where
	extract(dow
from
	dt) not in (6, 0)
	),
	hk_holidays (hk_holiday) as (
select
	date
from
	datetime.special_date sd
where
	is_hk_public_holiday = true
	),
trading_days (trading_day) as (
select
	weekday
from
	weekdays
except
select
	hk_holiday
from
	hk_holidays)
select
	trading_day
from
	trading_days
order by
	trading_days ;