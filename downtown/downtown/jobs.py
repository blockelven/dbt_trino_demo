from dagster import OpExecutionContext, job, op

from .resources import TrinoResource

@op()
def create_scheme_op(context: OpExecutionContext, trino: TrinoResource):
    default = trino.execute("create schema if not exists warehouse.default with (location = 's3a://warehouse/default')")
    context.log.info(f"create default schema: {default}")
    bronze = trino.execute("create schema if not exists warehouse.bronze with (location = 's3a://warehouse/bronze')")
    context.log.info(f"create bronze schema: {bronze}")
    silver = trino.execute("create schema if not exists warehouse.silver with (location = 's3a://warehouse/silver')")
    context.log.info(f"create silver schema: {silver}")
    gold = trino.execute("create schema if not exists analytics.gold")
    context.log.info(f"create gold schema: {gold}")
    
def drop_all_tables_in_schema(context, trino, schema_name):
    context.log.info(f"schema: {schema_name}")
    tables = trino.execute(f"show tables from {schema_name}")
    for table in tables:
        drop_statement = f"drop table if exists {schema_name}.{table[0]}"
        context.log.info(f"{drop_statement}")
        trino.execute(drop_statement)

@op()
def drop_tables_op(context: OpExecutionContext, trino: TrinoResource):
    drop_all_tables_in_schema(context, trino, "analytics.gold")
    drop_all_tables_in_schema(context, trino, "warehouse.silver")
    drop_all_tables_in_schema(context, trino, "warehouse.bronze")

@job()
def create_scheme_job():
    create_scheme_op()

@job()
def drop_tables_job():
    drop_tables_op()
