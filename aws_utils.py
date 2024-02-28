import awswrangler as wr
from backend.api.lib.db import conn
import sqlalchemy
from settings import S3_PARTITIONED_PATH, S3_RAW_PATH, GLUE_DB, TABLE_PATH
import boto3
import pandas as pd

# overwrite vs append
# when not partitioning, don't need dataset=True

# find last trade id
# add new records to...
    # store in s3 parquet
    # crawl aka store parquet metadata
    # does this update glue db?
    # partition by politicians/stocks (same process for both of these as all trade records but with partition? )
# what else do I need to update? store_parquet_metadata (information about table schema?)
# db currently returning no records

def find_last_trade_id_in_aws():
    df = wr.athena.read_sql_query(
        sql="SELECT max(id) as last_transaction_id FROM trades;",
        database=GLUE_DB)
    return df.last_transaction_id[0]

def get_data(id):
    query = f"""select * from trades where id > {id};"""
    df = pd.read_sql_query(query, con = conn)
    return df

def write_to_s3(df, path=TABLE_PATH):
    boto3.setup_default_session(region_name="us-west-2")
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
        path=TABLE_PATH,
        database=GLUE_DB,
        table=table_name,
        dataset=True,
        mode='append')
    return display_schema(table_name)

def display_schema(table_name):
    return wr.catalog.table(database=GLUE_DB, table=table_name)

def read_from_db(query):
    boto3.setup_default_session(region_name="us-west-2")
    return wr.athena.read_sql_query(query, database="trades")