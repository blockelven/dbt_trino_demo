with raw_data as (
	select 

		date as _c0, 
		symbol as _c1,
		open as _c2,
		high as _c3,
		low as _c4,
		close as _c5,
		volume as _c6,
		dividends as _c7,
		"stock splits" as _c8

		from {{ source('bronze', 'raw_yahoo_finance') }}
)
select
		_c0 as dt,
		trim(_c1) as symbol,
		_c2 as price_open,
		_c3 as price_high,
		_c4 as price_low,
		_c5 as price_close,
		_c6 as volume,
		_c7 as dividends,
		_c8 as splits						
		from raw_data
