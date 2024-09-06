with final as (
	select * from {{ ref("bronze__in_yahoo_finance") }} where symbol = 'AAPL'
)

select * from final
