import pdfplumber
import pandas as pd
import urllib3
import io
from backend.api.lib.db import add_record_to_house_trades, check_report_link_existence, add_report_record

class ReadHousePDF:
    def coerce_purchase_sold_row(self, column):
        try:
            value = column.split('\n')[0]
            return value
        except:
            return column

    def transform_raw_table_data(self, table):
        try:
            df = pd.DataFrame(table)
            df[3] = df[3].map(self.coerce_purchase_sold_row)
            purchased_sold = df[3].isin(['P', 'S', 'SP', 'E', 'S (partial)'])
            df[2] = df[2].str.replace('\x00', '')
            df = df[purchased_sold]
            return df.iloc[:,:7]
        except Exception as Error:
            print(Error)

    def read_pdfs(self, reports):
        for report in reports:
            if not self.verify_new_report(report): continue
            pages = self.extract_pdf_pages(report)
            for page in pages:
                pre_processed_table = self.pre_process_table_data(page)
                try:
                    all_row_data = []
                    for index, row in pre_processed_table.iterrows():
                        table_data = [row[i] for i in range(1,7)]
                        table_data.insert(1, report['name'])
                        all_row_data.append(table_data)
                        add_record_to_house_trades(table_data)
                except Exception as Error:
                    print(Error)

    def extract_pdf_pages(self, report):
        http = urllib3.PoolManager()
        temp = io.BytesIO()
        temp.write(http.request("GET", report['report_link']).data)
        pdf = pdfplumber.open(temp)
        pages = pdf.pages
        return pages
    
    def verify_new_report(self, report):
        exists = check_report_link_existence(report['report_link'])
        if exists: return False
        add_report_record(report['report_link'])
        return True

    def pre_process_table_data(self, page):
        settings = page.debug_tablefinder()
        col_lines = [line[0] for line in settings.__dict__['cells']]
        table_settings = {
            "vertical_strategy": "lines", 
            "horizontal_strategy": "lines",
            "explicit_vertical_lines": col_lines
        }
        table = page.extract_table(table_settings = table_settings)
        pre_processed_table = self.transform_raw_table_data(table)
        return pre_processed_table