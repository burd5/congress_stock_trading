import camelot
from settings import USER, DATABASE
from api.lib.db import cursor, add_record_to_database, check_record_existence
from api.models.stock import Stock
from api.models.politician import Politician
import re
import traceback

class ReadHousePDF:
    def __init__(self):
        self.rejected_stock_pdfs = set()
        self.rejected_stock_markers = set()
        self.rejected_politicians = set()
        self.rejected_column_pdfs = set()

    def read_pdf_table_data(self, report:dict, col_size: list):
        try:
            tables = camelot.read_pdf(report['report_link'], pages='all', flavor='stream', row_tol=20, columns=col_size, split_text=True, strip_text='\n')
            self.process_table_rows(report, tables)
        except Exception as error:
            print(traceback.format_exc(), error)
            self.rejected_column_pdfs.add(report['report_link'])
            
    def process_table_rows(self, report: dict, tables: object):
        politician_info = self.coerce_report_data(report)
        for table in tables:
            table_rows = table.df
            for row in table_rows.itertuples():
                self.process_row_data(row, report, table, politician_info)

    def process_row_data(self, row: tuple, report: dict, table: object, politician_info: dict):
        if row._3 in ['S', 'P', 'SP', 'E']:
            formatted_row = self.coerce_row_data(row)
            status = self.validate_data(report, table, formatted_row)
            if status: self.check_for_stock_and_politician_match_in_db(formatted_row, report, politician_info)
                
    def check_for_stock_and_politician_match_in_db(self, formatted_row, report, politician_info):
        politician = self.validate_politician_object(formatted_row, report, politician_info)
        stock = self.validate_stock_object(formatted_row, report, politician_info)
        table_data = [stock, politician] + formatted_row[1:]
        if politician and stock: 
            add_record_to_database(table_data, USER, DATABASE)
        self.remove_link_from_rejected_pdfs_if_successfully_scraped(report)

    def remove_link_from_rejected_pdfs_if_successfully_scraped(self, report):
        try:
            self.rejected_column_pdfs.remove(report['report_link'])
            print('link removed')
        except:
            print('link not in rejected pdfs')
    
    def validate_politician_object(self, formatted_row: list, report: dict, politician_info: dict):
        politician_by_name = Politician.find_by_name_house(politician_info['name'], cursor)
        if not politician_by_name:
            politician_by_office = Politician.find_by_office(politician_info['name'], politician_info['office'], cursor)
            if not politician_by_office:
                self.rejected_politicians.add(politician_info['name'])
                return None
            return politician_by_office.id
        return politician_by_name.id
        

    def validate_stock_object(self, formatted_row: list, report: dict, politician_info: dict):
        stock_marker = self.find_stock_marker(formatted_row[0])
        if not stock_marker: return None
        stock = Stock.find_by_stock_marker(stock_marker.upper(), cursor)
        if not stock:
            self.rejected_stock_markers.add(stock_marker)
            self.rejected_stock_pdfs.add(report['report_link'])
            return None
        return stock.id

    def read_pdf_reports(self, reports:list, col_size: list):
        for report in reports:
            try:
                self.read_pdf_table_data(report, col_size)
            except UserWarning:
                print("Can't use image based file")
        return [self.rejected_stock_pdfs, self.rejected_politicians, self.rejected_stock_markers, self.rejected_column_pdfs]

    def parse_politician_name(self, report:dict):
        name_split = report['name'].split(', Hon.. ')
        if len(name_split) == 1: return name_split[0]
        check_for_middle = name_split[1].split(' ')
        if len(check_for_middle) > 1:
            full_name = ' '.join([check_for_middle[0], name_split[0]])
        else:
            full_name = ' '.join(name_split[::-1])
        return full_name

    def find_stock_marker(self, stock_description:str):
        stock_marker = re.search(r'\((.*?)\)', stock_description)
        return stock_marker.group(1) if stock_marker else None

    def validate_data(self, report: dict, table: object, row: tuple):
        if row[1] == '' or len(row[1]) > 2:
            print('Error with purchase or sold column', row[1])
            print(report['report_link'])
            return False
        elif not self.check_date_format(row[2]):
            print('Error with date columns', row[2])
            print(report['report_link'])
            self.rejected_column_pdfs.add(report['report_link'])
            return False
        elif '$' not in row[3]:
            print('Error with amount column', row[3])
            print(report['report_link'])
            return False
        return True
    
    def check_date_format(self, date: str):
        regex = re.compile("[0-9]{4}\-[0-9]{2}\-[0-9]{2}")
        match = re.match(regex, date)
        if not match:
            return False
        return True

    def coerce_report_data(self, report: dict):
        report['name'] = self.parse_politician_name(report)
        report['office'] = report['office'].replace('0', '')
        politician_info = {k:v for k,v in report.items() if k != 'report_link'}
        return politician_info

    def coerce_row_data(self, row: tuple):
        row_list = list(row)
        row_list.pop(-3)
        formatted_row = row_list[2:-1]
        formatted_row[2] = self.convert_to_year_month_date(formatted_row[2])
        return formatted_row

    def convert_to_year_month_date(self, date_str: str):
        date = date_str.split('/')
        for i,num in enumerate(date):
            if len(num) == 1 and int(num):
                date[i] = f'0{num}'
        new_date = '-'.join([date[-1], date[0], date[1]])
        return new_date