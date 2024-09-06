from dagster import Definitions, define_asset_job, EnvVar
from dagster_dbt import DbtCliResource

from .jaffle_shop_assets import jaffle_shop_dbt_assets, order_count_chart, raw_customers
from .bronze_assets import raw_yahoo_finance, stocks_bronze_dbt_assets
from .jobs import create_scheme_job, drop_tables_job
from .project import jaffle_shop_project, stock_project
from .resources import IcebergResource, TrinoResource
from .schedules import schedules

jaffle_shop_job = define_asset_job(
    name="jaffle_shop_job", 
    selection=[
        "raw_customers",
        "raw_orders",
        "raw_payments",
        "stg_customers",
        "stg_orders",
        "stg_payments",
        "customers",
        "orders",
    ])

defs = Definitions(
    assets=[raw_customers, jaffle_shop_dbt_assets, order_count_chart, raw_yahoo_finance, stocks_bronze_dbt_assets],
    jobs=[jaffle_shop_job, create_scheme_job, drop_tables_job],
    schedules=schedules,
    resources={
        "dbt_shop": DbtCliResource(project_dir=jaffle_shop_project),
        "dbt_stock": DbtCliResource(project_dir=stock_project),
        "trino": TrinoResource(
            host=EnvVar("TRINO_HOST"), 
            port=EnvVar("TRINO_PORT"), 
            user=EnvVar("TRINO_USER"), 
            password=EnvVar("TRINO_PASSWORD")
        ),
        "iceberg": IcebergResource(
            name=EnvVar("ICE_NAME"), 
            catalog_uri=EnvVar("ICE_CATALOG_URI"),
            warehouse_path=EnvVar("ICE_WH_PATH"),
            s3_endpoint=EnvVar("ICE_S3_ENDPOINT"),
            s3_ak=EnvVar("ICE_S3_AK"),
            s3_sk=EnvVar("ICE_S3_SK")
        )
    },
)
