from data.models.scrape_house_trades import HouseScraper
from data.models.house_stock_adapter import ReadHousePDF
from data.models.rejected_information import RejectedInfo
from api import create_app
from settings import DATABASE, USER, PASSWORD

app = create_app(dbname=DATABASE, user=USER, password=PASSWORD)

app.run(debug=True)




