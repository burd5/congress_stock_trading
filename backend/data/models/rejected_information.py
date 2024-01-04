from data.models.scrape_house_trades import HouseScraper
from data.models.house_stock_adapter import ReadHousePDF
#['88,267.5,315,385,444,526']

class RejectedInfo:
    def scrape_per_year(self, year_identifier: str, number_of_pages: int):
        columns = [['89,228,285,362,423,509'], ['88,265.5,315,385,444,535'], ['88,260,315,381,448,545'], ['107,256,323,391,456, 550']]

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