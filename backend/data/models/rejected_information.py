from data.models.scrape_house_trades import HouseScraper
from data.models.house_stock_adapter import ReadHousePDF

class RejectedInfo:
    def scrape_per_year(self, year_identifier: str, number_of_pages: int):
        columns = [['89,228,285,362,423,509'], ['91,259,322.2,378.7,443.6,520'], ['88,265.5,315,385,444,535'], ['88,260,315,381,448,545'], ['107,256,323,391,456,550'], ['105,264.9,328.9,386,450.1,522.5'], ['91,242,308.8,361.7,427,501'], ['91,266.9,331,383.8,449.9,528']]

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
    
# [['https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2022/20020182.pdf', 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2022/20020629.pdf', 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2022/20020552.pdf', 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2022/20020179.pdf', 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2022/20020564.pdf', 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2022/20020443.pdf', 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2022/20020153.pdf', 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2022/20020718.pdf', 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2022/20020321.pdf', 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2022/20020355.pdf', 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2022/20020197.pdf', 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2022/20020323.pdf', 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2022/20020446.pdf', 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2022/20020648.pdf', 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2022/20020462.pdf', 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2022/20020322.pdf'], ['Greg Steube', 'Christopher Jacobs', 'Michael Garcia', 'Scott Franklin', 'Richard Allen'], ['AAIC$B', 'SCHH', 'FLGB', 'CORPORATEBOND', 'VOLVY', 'FHLC', 'IAA', 'DWDP', 'XLE', 'IS', 'FPE', 'PSQ', 'FAS'], []

# ['Daniel Goldman', 'Lesko, Debbie', 'Cathy Rodgers', 'Felix Moore', 'Jeff Jackson', 'James Hill', 'Rick Larsen', 'C. Franklin'], ['AQUA', 'FQAL', 'IYY', '36966R5P7', 'MATURITY08/10/2023', 'INSW.V', 'Belgium', 'EMXC', 'AAIC$B', 'MATURITY08/24/2023', 'IWD', 'JGCCF', 'NCMGF', '912796QV4', '912796ZP7', 'IJR', 'BAC.PL', '13-Week Matures4/13/2023', 'MLYNF', 'FMBA', '91282CDR9', 'GLAS Funds,LP', '6-Month, Matures06/27/2024', 'MNRL', '13-Week, Matures5/4/2023', 'AMLP', 'SGENX', 'FMCSX', 'VIV.V', 'GLAS Funds, LP', '4-week, Matures6/6/2023', 'NPPNY', '4-Week Matures2/14/2023', 'RSP', 'SCHD', 'REIT', 'PFF', 'SYNH', 'IGSB', 'SHY', 'OCLCF', '4-Week, Matures10/3/2023', 'CEMCF', 'SCHP', '3-month, Matures11/9/2023', 'FDN', '13-Week, Matures01/11/2024', '8-week, Matures8/29/23', '4-Week, Matures8/1/23', 'IVV', '912797LL9', 'SHV', 'Matures12/14/2023', '91282CFN6', 'FHLC', '912796QX0', '912796U49', 'PSDTX', '91282CFG1', '912796X87', '912796YH6', '912796YJ2', '912796XQ7', 'HCRB', 'CWEN.A', '91282CEG2', '912796SH3', '912796WX3', '912796U31']
    
