from data.models.scrape_house_trades import HouseScraper
from data.models.house_stock_adapter import ReadHousePDF
from data.models.rejected_information import RejectedInfo
# from console import results_2018, results_2019, results_2020, results_2021, results_2022, results_2023
from api import create_app
from settings import DATABASE, USER, PASSWORD

# print(results_2018.scrape_per_year('12', 158))
# print(results_2019.scrape_per_year('13', 178))
# print(results_2020.scrape_per_year('14', 169))
# print(results_2021.scrape_per_year('15', 148))
# print(results_2022.scrape_per_year('16', 138))
# print(results_2023.scrape_per_year('17', 59))

app = create_app(dbname=DATABASE, user=USER, password=PASSWORD)

app.run(debug=True)




