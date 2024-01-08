from data.models.scrape_house_trades import HouseScraper
from data.models.house_stock_adapter import ReadHousePDF
from data.models.rejected_information import RejectedInfo
from data.models.scrape_senate_trades import SenateScraper
from data.models.senate_trade_adapter import ReadTransactionTableData
from data.models.senate_trade_adapter import ReadTransactionTableData
import api.models as api_models
from api.lib.db import cursor, conn
import camelot

# ReadTransactionTableData().process_transactions([{'name': 'Lamar Alexander', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/a5ea65ef-3943-4944-b192-988ab6adaa21/'}, {'name': 'John A Barrasso', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/265964e0-3d22-4a52-af4f-37916b56390d/'}, {'name': 'Michael F Bennet', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/cd2add48-f2bc-42bc-acbd-d8f7b502eae1/'}])

# results = ReadHousePDF().read_pdf_reports(scraped_reports, col)

# results_2018 = RejectedInfo()
# results_2019 = RejectedInfo()
# results_2020 = RejectedInfo()
# results_2021 = RejectedInfo()
# results_2022 = RejectedInfo()
# results_2023 = RejectedInfo()

scraped_senate_reports = SenateScraper(79).initialize_webscrape()
print(ReadTransactionTableData().process_transactions(scraped_senate_reports))






