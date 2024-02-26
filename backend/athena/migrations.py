import awswrangler as wr
from settings import GLUE_DB, S3_RAW_PATH

databases = wr.catalog.databases()

def create_db():
    wr.catalog.create_database(GLUE_DB)

def delete_db():
    wr.catalog.delete_database(
        name=GLUE_DB
    )

def crawl_dataset(table_name):
    res = wr.s3.store_parquet_metadata(
        path=S3_RAW_PATH,
        database=GLUE_DB,
        table=table_name)
    return display_schema(table_name)
    
def display_schema(table_name):
    return wr.catalog.table(database=GLUE_DB, table=table_name)