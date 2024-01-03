from data.models.scrape_house_stocks import HouseScraper
from data.models.read_house_trade_pdfs import ReadHousePDF
import api.models as api_models
from api.lib.db import cursor, conn

def scrape_per_year(year_identifier, number_of_pages):
    columns = [['89,228,285,362,423,509'], ['88,265.5,315,385,444,535'], ['88,260,315,381,448,545'], ['88,267.5,315,385,444,526'], ['107,256,323,391,456, 550']]

    rejected_stock_pdfs = []
    rejected_politicians = []
    rejected_stock_markers = []
    rejected_column_pdfs = []

    scraped_reports = HouseScraper().initialize_webscrape(year_identifier, number_of_pages)
    for col in columns:
        results = ReadHousePDF().read_pdf_reports(scraped_reports, col)
        [rejected_stock_pdfs.append(result) for result in results[0] if result not in rejected_stock_pdfs]
        [rejected_politicians.append(result) for result in results[1] if result not in rejected_politicians]
        [rejected_stock_markers.append(result) for result in results[2] if result not in rejected_stock_markers]
        [rejected_column_pdfs.append(result) for result in results[3] if result not in rejected_column_pdfs]
       
    return [rejected_stock_pdfs, rejected_politicians, rejected_stock_markers, rejected_column_pdfs]

results_2018 = scrape_per_year('12', 158)
results_2019 = scrape_per_year('13', 178)
results_2020 = scrape_per_year('14', 169)
results_2021 = scrape_per_year('15', 148)
results_2022 = scrape_per_year('16', 137)
results_2023 = scrape_per_year('17', 59)

records_2018 = results_2018





