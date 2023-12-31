from data.models.scrape_house_stocks import HouseScraper
from data.models.read_house_trade_pdfs import ReadHousePDF

import api.models as api_models
from api.lib.db import cursor, conn


# [['89,228,285,362,423,509'], ['88,260,315,381,448,545'], ['88,265.5,315,385,444,535'], ['88,265.5,315,385,444,526'], ['88,267.5,315,385,444,526'] ['107,256,323,391,456, 550']]
# ReadHousePDF().read_pdf_reports(transaction_reports, ['89,228,285,362,423,509'])
# ReadHousePDF().read_pdf_reports(transaction_reports, ['88,265.5,315,385,444,535'])
# ReadHousePDF().read_pdf_reports(transaction_reports, ['88,265.5,315,385,444,535'])
# ReadHousePDF().read_pdf_reports(transaction_reports, ['88,267.5,315,385,444,535'])
# ReadHousePDF().read_pdf_reports(transaction_reports, ['107,256,323,391,456, 550'])

# add filing year argument to initialize webscrape
# continue web_scraping other column sizes using rejected_column_pdfs

scraped_reports = HouseScraper().initialize_webscrape()
rejected_stock_pdfs, rejected_politicians, rejected_stocks, rejected_column_pdfs = ReadHousePDF().read_pdf_reports(scraped_reports, ['89,228,285,362,423,509'])

print(rejected_stock_pdfs, rejected_politicians, rejected_stocks, rejected_column_pdfs)








