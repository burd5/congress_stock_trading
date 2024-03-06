from backend.data.models.scrape_house_trades import HouseScraper
from backend.data.models.scrape_senate_trades import SenateScraper
from backend.athena.migrations import create_db, crawl_dataset, display_schema
from backend.data.models.house_pdf_plumber_scraper import ReadHousePDF
from backend.data.models.senate_pdf_plumber_scraper import TransformSenateRecordsData


scraped_reports = HouseScraper().initialize_webscrape()
adapter = ReadHousePDF().read_pdfs(scraped_reports)

scraped_senate_reports = SenateScraper().initialize_webscrape()
TransformSenateRecordsData().process_transactions(scraped_senate_reports)



