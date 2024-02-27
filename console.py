from backend.data.models.scrape_house_trades import HouseScraper
from backend.data.models.house_stock_adapter import ReadHousePDF
from backend.data.models.rejected_information import Scrape_Coerce_House_Records
from backend.data.models.scrape_senate_trades import SenateScraper
from backend.data.models.senate_trade_adapter import TransformSenateRecordsData
import backend.api.models as api_models
from backend.athena.migrations import create_db, crawl_dataset, display_schema

# house_scraper = Scrape_Coerce_House_Records()
# house_scraper.scrape()

scraped_senate_reports = SenateScraper().initialize_webscrape()
print(TransformSenateRecordsData().process_transactions(scraped_senate_reports))



