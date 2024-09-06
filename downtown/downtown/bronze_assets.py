from dagster import AssetExecutionContext, MetadataValue, asset, Config
from dagster_dbt import DbtCliResource, dbt_assets, get_asset_key_for_model, DagsterDbtTranslator
import pandas as pd
import yfinance as yf

from .resources import IcebergResource
from .project import stock_project
from typing import Any
import pyarrow as pa

class StockDbtTranslator(DagsterDbtTranslator):
    def get_group_name( # type: ignore
        self, dbt_resource_props: dict[str, Any]
    ) -> str | None:
        return "stock"

@asset(compute_kind="python")
def raw_yahoo_finance(context: AssetExecutionContext, iceberg: IcebergResource):
    symbols = ['AAPL', 'GOOGL', 'ORCL', 'MSFT', 'CRM', 'IBM', 'AMZN', 'GC=F']
    start_date = '2000-01-01'
    end_date = '2024-06-30'
    dfs = []
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date)
        df.insert(0, 'Symbol', symbol)
        dfs.append(df)
    total_df = pd.concat(dfs).sort_index()
    context.log.info(f'{total_df.dtypes}')
    total_df.index = total_df.index.tz_localize(None) # type: ignore
    df = pa.Table.from_pandas(total_df)
    context.log.info(f'{df.schema}')
    table = iceberg.catalog.create_table_if_not_exists("bronze.raw_yahoo_finance", schema=df.schema)
    table.append(df)
    context.add_output_metadata({"num_rows": total_df.shape[0]})


@dbt_assets(manifest=stock_project.manifest_path, dagster_dbt_translator=StockDbtTranslator())
def stock_dbt_assets(context: AssetExecutionContext, dbt_stock: DbtCliResource):
    yield from dbt_stock.cli(["build"], context=context).stream().fetch_row_counts().fetch_column_metadata()

