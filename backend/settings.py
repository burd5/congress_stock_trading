from dotenv import load_dotenv
import os

load_dotenv()

DATABASE=os.getenv('DATABASE')
USER=os.getenv('USER')
PASSWORD=os.getenv('PASSWORD')
TEST_DB=os.getenv('TEST_DB')