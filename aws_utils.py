import awswrangler as wr
from api.lib.db import conn
import sqlalchemy
from settings import S3_PARTITIONED_PATH, S3_RAW_PATH, GLUE_DB

query = """select * from trades;"""
# df = alchemy stuff

def find_last_stock_id():
    df = wr.athena.read_sql_query(
        sql="SELECT max(id) as last_transaction FROM trades;",
        database=GLUE_DB)
    return df.fillna('').last_end_date[0]

def write_to_s3(df, partition_cols, mode='append'):
    wr.s3.to_parquet(df = df, path = S3_PARTITIONED_PATH, mode = mode, dataset = True, partition_cols = partition_cols)