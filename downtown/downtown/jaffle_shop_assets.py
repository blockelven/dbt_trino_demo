import os
from typing import Any

from dagster import AssetExecutionContext, MetadataValue, asset
from dagster_dbt import (
    DagsterDbtTranslator,
    DbtCliResource,
    dbt_assets,
    get_asset_key_for_model,
)
import duckdb
import pandas as pd
import plotly.express as px

from .project import jaffle_shop_project


duckdb_db_path = jaffle_shop_project.project_dir.joinpath("tutorial.duckdb")

class JaffleDbtTranslator(DagsterDbtTranslator):
    def get_group_name( # type: ignore
        self, dbt_resource_props: dict[str, Any]
    ) -> str | None:
        return "jaffle_shop"


@asset(compute_kind="python")
def raw_customers(context: AssetExecutionContext) -> None:
    data = pd.read_csv("https://docs.dagster.io/assets/customers.csv")
    connection = duckdb.connect(os.fspath(duckdb_db_path))
    connection.execute("create schema if not exists jaffle_shop")
    connection.execute(
        "create or replace table jaffle_shop.raw_customers as select * from data"
    )

    context.add_output_metadata({"num_rows": data.shape[0]})


@dbt_assets(manifest=jaffle_shop_project.manifest_path, dagster_dbt_translator=JaffleDbtTranslator())
def jaffle_shop_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

@asset(
    compute_kind="python",
    deps=get_asset_key_for_model([jaffle_shop_dbt_assets], "customers"),
    group_name='jaffle_shop'
)
def order_count_chart(context: AssetExecutionContext):
    connection = duckdb.connect(os.fspath(duckdb_db_path))
    customers = connection.sql("select * from customers").df()

    fig = px.histogram(customers, x="number_of_orders")
    fig.update_layout(bargap=0.2)
    save_chart_path = duckdb_db_path.parent.joinpath("order_count_chart.html")
    fig.write_html(save_chart_path, auto_open=True)

    # tell Dagster about the location of the HTML file,
    # so it's easy to access from the Dagster UI
    context.add_output_metadata(
        {"plot_url": MetadataValue.url("file://" + os.fspath(save_chart_path))}
    )
