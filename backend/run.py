from data.models.scrape_house_stocks import HouseScraper
from data.models.read_house_trade_pdfs import ReadHousePDF
from data.models.rejected_information import RejectedInfo
from console import results_2018, results_2019, results_2020, results_2021, results_2022, results_2023

results_2018.scrape_per_year('12', 158)
results_2019.scrape_per_year('13', 178)
results_2020.scrape_per_year('14', 169)
results_2021.scrape_per_year('15', 148)
results_2022.scrape_per_year('16', 137)
results_2023.scrape_per_year('17', 59)

