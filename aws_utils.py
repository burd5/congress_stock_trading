import awswrangler as wr
from backend.api.lib.db import conn
import sqlalchemy
from settings import S3_PARTITIONED_PATH, GLUE_DB
import pandas as pd
# boto3.setup_default_session(region_name="us-west-2")

def find_last_trade_id_in_aws():
    df = wr.athena.read_sql_query(
        sql="SELECT max(id) as last_transaction_id FROM trades;",
        database=GLUE_DB)
    return df.last_transaction_id[0]

def get_data_from_local_postgres_db(id):
    query = f"""select * from trades where id > {id};"""
    df = pd.read_sql_query(query, con = conn)
    return df

def write_to_s3(df, path=S3_PARTITIONED_PATH):
    response = wr.s3.to_parquet(
        df=df, 
        path=path,
        partition_cols=['politician_id'],
        dataset=True,
        mode="append"
    )
    return response

def crawl_dataset(table_name='trades'):
    res = wr.s3.store_parquet_metadata(
        path=S3_PARTITIONED_PATH,
        database=GLUE_DB,
        table=table_name,
        dataset=True,
        mode='append')
    return display_schema(table_name)

def display_schema(table_name):
    return wr.catalog.table(database=GLUE_DB, table=table_name)
