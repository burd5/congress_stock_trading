from backend.data.models.scrape_house_trades import HouseScraper
from backend.data.models.house_stock_adapter import ReadHousePDF

class RejectedInfo:
    def scrape(self):
        columns = [['89,228,285,362,423,509'], ['91,259,322.2,378.7,443.6,520'], ['88,265.5,315,385,444,535'], ['88,260,315,381,448,545'], ['107,256,323,391,456,550'], ['105,264.9,328.9,386,450.1,522.5'], ['91,242,308.8,361.7,427,501'], ['91,266.9,331,383.8,449.9,528']]

        rejected_stock_pdfs = []
        rejected_politicians = []
        rejected_stock_markers = []
        rejected_column_pdfs = []

        scraped_reports = HouseScraper().initialize_webscrape()
        for col in columns:
            results = ReadHousePDF().read_pdf_reports(scraped_reports, col)
            [rejected_stock_pdfs.append(result) for result in results[0] if result not in rejected_stock_pdfs]
            [rejected_politicians.append(result) for result in results[1] if result not in rejected_politicians]
            [rejected_stock_markers.append(result) for result in results[2] if result not in rejected_stock_markers]
            [rejected_column_pdfs.append(result) for result in results[3] if result not in rejected_column_pdfs]
        
        return [rejected_stock_pdfs, rejected_politicians, rejected_stock_markers, rejected_column_pdfs]
    
