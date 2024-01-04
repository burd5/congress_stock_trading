from data.models.scrape_house_trades import HouseScraper
from data.models.house_stock_adapter import ReadHousePDF
from data.models.rejected_information import RejectedInfo
from console import results_2018, results_2019, results_2020, results_2021, results_2022, results_2023

print(results_2018.scrape_per_year('12', 60))
print(results_2019.scrape_per_year('13', 10))
print(results_2020.scrape_per_year('14', 10))
print(results_2021.scrape_per_year('15', 10))
print(results_2022.scrape_per_year('16', 10))
print(results_2023.scrape_per_year('17', 10))




