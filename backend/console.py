from data.models.scrape_house_trades import HouseScraper
from data.models.house_stock_adapter import ReadHousePDF
from data.models.rejected_information import RejectedInfo
from data.models.scrape_senate_trades import SenateScraper
from data.models.senate_trade_adapter import ReadTransactionTableData
from data.models.senate_trade_adapter import ReadTransactionTableData
import api.models as api_models

results_2024 = RejectedInfo()
results_2024.scrape_per_year()

scraped_senate_reports = SenateScraper(79).initialize_webscrape()
print(ReadTransactionTableData().process_transactions(scraped_senate_reports))






