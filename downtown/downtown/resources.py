from dagster import ConfigurableResource, InitResourceContext
from contextlib import contextmanager
from pydantic import PrivateAttr
from trino.dbapi import connect as trino_connection, Connection as TrinoConnection

from pyiceberg.catalog import load_catalog, Catalog

@contextmanager
def get_connection(host: str, port: str, user: str):
    conn = trino_connection(host=host, port=port, user=user)
    yield conn
    conn.close()

class TrinoResource(ConfigurableResource):
    host: str
    port: str
    user: str
    password: str

    _db_conn: TrinoConnection = PrivateAttr()

    @contextmanager
    def yield_for_execution(self, context: InitResourceContext):
        with get_connection(self.host, self.port, self.user) as conn:
            self._db_conn = conn
            yield self

    def execute(self, sql: str):
        cursor = self._db_conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
       

class IcebergResource(ConfigurableResource):
    name: str
    catalog_uri: str
    warehouse_path: str
    s3_endpoint: str
    s3_ak: str
    s3_sk: str

    @property
    def catalog(self) -> Catalog:
        catalog_ = load_catalog(
            self.name,
            **{
            "py-catalog-impl": "pyiceberg.catalog.sql.SqlCatalog",
            "uri": self.catalog_uri, 
            "warehouse": self.warehouse_path,
            "s3.endpoint": self.s3_endpoint,
            "s3.access-key-id": self.s3_ak,
            "s3.secret-access-key": self.s3_sk

            }
        )
        return catalog_

