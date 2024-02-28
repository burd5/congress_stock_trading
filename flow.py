from prefect import task, flow
from backend.data.models.rejected_information import Scrape_Coerce_House_Records
from backend.data.models.scrape_senate_trades import SenateScraper
from aws_utils import find_last_trade_id_in_aws


# scrape senate and house records
@task
def scrape_house_and_senate_records():
    pass

# find last record added in s3
@task
def find_last_trade_id():
    return find_last_trade_id_in_aws()

# based on last record, partition and add new records to s3 bucket

# make sense to partition stocks/politicians but keep all records in trades table?



@flow
def scrape_records_and_add_to_s3():
    pass
