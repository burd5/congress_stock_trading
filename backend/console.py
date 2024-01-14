from data.models.scrape_house_trades import HouseScraper
from data.models.house_stock_adapter import ReadHousePDF
from data.models.rejected_information import RejectedInfo
from data.models.scrape_senate_trades import SenateScraper
from data.models.senate_trade_adapter import ReadTransactionTableData
from data.models.senate_trade_adapter import ReadTransactionTableData
import api.models as api_models
from api.lib.db import cursor, conn

# results_2018 = RejectedInfo()
# results_2019 = RejectedInfo()
# results_2020 = RejectedInfo()
# results_2021 = RejectedInfo()
# results_2022 = RejectedInfo()
# results_2023 = RejectedInfo()

scraped_senate_reports = SenateScraper(79).initialize_webscrape()
print(ReadTransactionTableData().process_transactions(scraped_senate_reports))






