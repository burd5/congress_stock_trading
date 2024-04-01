import awswrangler as wr
from backend.api.lib.db import conn
from settings import GLUE_DB
import pandas as pd
import boto3

def find_last_trade_id_in_aws(table):
    df = wr.athena.read_sql_query(
        sql=f"SELECT * FROM {table};",
        database='congress_trades')
    return df

def get_data_from_local_postgres_db(table_name):
    query = f"""select * from {table_name};"""
    df = pd.read_sql_query(query, con = conn)
    return df


def write_to_s3(df, bucket, partition_cols = ['politician_name']):
    response = wr.s3.to_parquet(
        df=df, 
        path=f"s3://congress-trades/{bucket}/",
        partition_cols=partition_cols,
        dataset=True,
        mode="append"
    )
    return response

def crawl_dataset(table_name, bucket):
    res = wr.s3.store_parquet_metadata(
        path=f"s3://congress-trades/{bucket}/",
        database="congress_trades",
        table=table_name,
        dataset=True,
        mode='append')
    return display_schema(table_name)

def display_schema(table_name):
    return wr.catalog.table(database=GLUE_DB, table=table_name)
