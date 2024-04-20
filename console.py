from backend.data.models.scrape_house_trades import HouseScraper
from backend.data.models.scrape_senate_trades import SenateScraper
from backend.data.models.house_pdf_plumber_scraper import ReadHousePDF
from backend.data.models.senate_pdf_plumber_scraper import TransformSenateRecordsData
# from backend.data.models.get_pol_images import get_members

# run on all house records and all senate records

scraped_reports = HouseScraper().initialize_webscrape()
house = ReadHousePDF()
house.read_pdfs(scraped_reports)

print('Finished running House Scraper')

scraped_senate_reports = SenateScraper().initialize_webscrape()
TransformSenateRecordsData().process_transactions(scraped_senate_reports)

print('Finished running Senate Scraper')

