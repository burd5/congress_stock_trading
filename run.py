from backend.data.models.scrape_house_trades import HouseScraper
from backend.data.models.house_stock_adapter import ReadHousePDF
from backend.data.models.rejected_information import RejectedInfo
from backend.api import create_app
from settings import DATABASE, USER, PASSWORD

app = create_app(dbname=DATABASE, user=USER, password=PASSWORD)

app.run(debug=True)




