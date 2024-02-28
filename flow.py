from prefect import task, flow
from backend.data.models.rejected_information import House_Records
from backend.data.models.scrape_senate_trades import SenateScraper
from backend.data.models.senate_trade_adapter import TransformSenateRecordsData
from aws_utils import find_last_trade_id_in_aws, get_data_from_local_postgres_db, write_to_s3, crawl_dataset


@task
def scrape_house_and_senate_records():
    # scrape house records, transform data, add to local postgres db
    House_Records().scrape()
    # scrape senate records
    scraped_senate_reports = SenateScraper().initialize_webscrape()
    # transform senate data and add to local postgres db
    TransformSenateRecordsData().process_transactions(scraped_senate_reports)

@task
def find_last_trade_id():
    # find last record (trade id) added in s3
    return find_last_trade_id_in_aws()

@task
def get_data(id):
    # get trade ids from local postgresdb that are larger than last trade id in s3 bucket
    return get_data_from_local_postgres_db(id)

@task
def upload_to_s3(df):
    # add records to s3 bucket
    return write_to_s3(df)

@task
def crawl_data():
    # recrawl partitioned data
    return crawl_dataset()

@flow
def scrape_records_and_add_to_s3():
    scrape_house_and_senate_records()
    id = find_last_trade_id()
    df = get_data(id)
    upload_to_s3(df)
    crawl_data()


if __name__ == "__main__":
    scrape_records_and_add_to_s3()