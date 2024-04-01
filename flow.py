from prefect import task, flow
from backend.data.models.scrape_house_trades import HouseScraper
from backend.data.models.scrape_senate_trades import SenateScraper
from backend.data.models.senate_pdf_plumber_scraper import TransformSenateRecordsData
from backend.data.models.house_pdf_plumber_scraper import ReadHousePDF


@task
def scrape_house_and_senate_records():
    # scrape house records, transform data, add to local postgres db
    scraped_reports = HouseScraper().initialize_webscrape()
    ReadHousePDF().read_pdfs(scraped_reports)
    # scrape senate records
    scraped_senate_reports = SenateScraper().initialize_webscrape()
    # transform senate data and add to local postgres db
    TransformSenateRecordsData().process_transactions(scraped_senate_reports)

@flow
def scrape_records_and_add_to_s3():
    scrape_house_and_senate_records()


if __name__ == "__main__":
    scrape_records_and_add_to_s3()