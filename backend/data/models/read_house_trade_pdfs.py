import camelot
import psycopg2
from settings import USER, DATABASE
from api.lib.db import cursor
from api.models.stock import Stock
from api.models.politician import Politician
import re

class ReadHousePDF:
    def __init__(self):
        self.rejected_stock_pdfs = set()
        self.rejected_stock_markers = set()
        self.rejected_politicians = set()
        self.rejected_column_pdfs = set()

    def read_pdf_table_data(self, report:dict, col_size):
        try:
            tables = camelot.read_pdf(report['report_link'], pages='all', flavor='stream', row_tol=20, columns=col_size, split_text=True, strip_text='\n')
            self.process_table_rows(report, tables)
        except:
            self.rejected_column_pdfs.add(report['report_link'])
            
    def process_table_rows(self,report,tables):
        politician_info = self.coerce_report_data(report)
        for table in tables:
            table_rows = table.df
            for row in table_rows.itertuples():
                self.process_row_data(row, report, table, politician_info)

    def process_row_data(self, row, report, table, politician_info):
        if row._3 in ['S', 'P', 'SP', 'E']:
            formatted_row = self.coerce_row_data(row)
            status = self.validate_data(report, table, formatted_row)
            if status:
                stock, politician = self.validate_stock_and_politician_objects(formatted_row, report, politician_info)
                table_data = [stock, politician] + formatted_row[1:]
                self.add_record_to_database(table_data, USER, DATABASE)
    
    def validate_stock_and_politician_objects(self, formatted_row, report, politician_info):
        politician = Politician.find_by_name_and_office(politician_info['name'], politician_info['office'], cursor)
        if not politician:
            self.rejected_politicians.add(politician_info['name'])
        stock_marker = self.find_stock_marker(formatted_row[0]).upper()
        stock = Stock.find_by_stock_marker(stock_marker, cursor)
        if not stock:
            self.rejected_stock_markers.add(stock_marker)
            self.rejected_stock_pdfs.add(report['report_link'])
        return stock.id, politician.id
    
    def add_record_to_database(self,record, user, database):
        conn = psycopg2.connect(user=user, database=database)
        cursor = conn.cursor()
        statement = """INSERT INTO trades (stock_id, politician_id, purchased_or_sold, transaction_date, notification_date, amount)
                                VALUES(%s, %s, %s, %s, %s, %s);"""
        # if not self.check_record_existence(record, user, database):
        print(statement, record)
        cursor.execute(statement, record)
        conn.commit()
        conn.close()

    def check_record_existence(self,record, user, database):
        conn = psycopg2.connect(user=user, database=database)
        cursor = conn.cursor()
        
        check_statement = """SELECT EXISTS(
                                SELECT 1 FROM trades
                                WHERE stock_id = %s 
                                AND politician_id = %s
                                AND purchased_or_sold = %s
                                AND transaction_date = %s 
                                AND notification_date = %s 
                                AND amount = %s
                            );"""
        cursor.execute(check_statement, record)
        exists = cursor.fetchone()[0]
        conn.close()
        return exists

    def read_pdf_reports(self, reports, col_size):
        for report in reports:
            try:
                self.read_pdf_table_data(report, col_size)
            except UserWarning:
                print("Can't use image based file")
        return [self.rejected_stock_pdfs, self.rejected_politicians, self.rejected_stock_markers, self.rejected_column_pdfs]

    def parse_politician_name(self, report:dict):
        name_split = report['name'].split(', Hon.. ')
        full_name = ' '.join(name_split[::-1])
        return full_name

    def find_stock_marker(self, stock_description:str):
        stock_marker = re.search(r'\((.*?)\)',stock_description).group(1)
        return stock_marker

    def validate_data(self, report, table, row):
        if row[1] == '' or len(row[1]) > 2:
            print('Error with purchase or sold column', row[1])
            print(report['report_link'])
            self.rejected_column_pdfs.add(report)
            return False
        elif not self.check_date_formats([row[2], row[3]]):
            print('Error with date columns', row[2], row[3])
            print(report['report_link'])
            self.rejected_column_pdfs.add(report)
        elif '$' not in row[4]:
            print('Error with amount column', row[4])
            print(report['report_link'])
            self.rejected_column_pdfs.add(report)
            return False
        return True
    
    def check_date_formats(self, dates):
        for date in dates:
            regex = re.compile("[0-9]{4}\-[0-9]{2}\-[0-9]{2}")
            match = re.match(regex, date)
            if not match:
                return False
        return True

    def coerce_report_data(self, report):
        report['name'] = self.parse_politician_name(report)
        report['office'] = report['office'].replace('0', '')
        politician_info = {k:v for k,v in report.items() if k != 'report_link'}
        return politician_info

    def coerce_row_data(self,row):
        formatted_row = (list(row[2:-1]))
        formatted_row[2] = self.convert_to_year_month_date(formatted_row[2])
        formatted_row[3] = self.convert_to_year_month_date(formatted_row[3])
        return formatted_row

    def convert_to_year_month_date(self,date_str):
        date = date_str.split('/')
        for i,num in enumerate(date):
            if len(num) == 1 and int(num):
                date[i] = f'0{num}'
        new_date = '-'.join([date[-1], date[0], date[1]])
        return new_date

