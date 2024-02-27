from prefect import task, flow
from backend.data.models.rejected_information import Scrape_Coerce_House_Records
from backend.data.models.scrape_senate_trades import SenateScraper

# find last record added in postgres


# scrape senate and house records
@task
def scrape_house_and_senate_records():
    pass

# based on last record, partition and add new records to s3 bucket


# update aws athena/glue to query new records


@flow
def scrape_records_and_add_to_s3():
    pass
