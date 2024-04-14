from dotenv import load_dotenv
import os

load_dotenv()

USER=os.getenv('USER')
PASSWORD=os.getenv('PASSWORD')
DATABASE=os.getenv('DB_NAME')
SUPA_USER=os.getenv('SUPA_USER')
SUPA_PASSWORD=os.getenv('SUPA_PASSWORD')
HOST=os.getenv('HOST')
TEST_DB=os.getenv('TEST_DB')
S3_RAW_PATH=os.getenv('S3_RAW_PATH')
S3_PARTITIONED_PATH=os.getenv('S3_PARTITIONED_PATH')
GLUE_DB=os.getenv('GLUE_DB')
RAW_DATABASE=os.getenv('RAW_DATABASE')
SUPA_CONN_URL=os.getenv('SUPA_CONN_URL')
SUPA_KEY=os.getenv('SUPA_KEY')
API_KEY=os.getenv('API_KEY')