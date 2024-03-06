from dotenv import load_dotenv
import os

load_dotenv()

DATABASE=os.getenv('DATABASE')
USER=os.getenv('USER')
PASSWORD=os.getenv('PASSWORD')
TEST_DB=os.getenv('TEST_DB')
S3_RAW_PATH=os.getenv('S3_RAW_PATH')
S3_PARTITIONED_PATH=os.getenv('S3_PARTITIONED_PATH')
GLUE_DB=os.getenv('GLUE_DB')
RAW_DATABASE=os.getenv('RAW_DATABASE')