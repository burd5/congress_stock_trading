from backend.api.models.politician import Politician
from backend.api.models.stock import Stock
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from settings import USER, DATABASE
from backend.api.lib.db import cursor, add_record_to_database, add_asset_record
soup = BeautifulSoup('html', 'lxml')

class ReadTransactionTableData:
    def process_transactions(self, transactions: list):
        driver = self.bypass_agree_statement()
        for transaction in transactions:
            self.read_table_data(transaction, driver)
        driver.quit()

    def bypass_agree_statement(self):
        driver = webdriver.Chrome()
        driver.get('https://efdsearch.senate.gov/search/')
        search_button = driver.find_element(By.XPATH, '//*[@id="agree_statement"]')
        search_button.click()
        time.sleep(2)
        return driver

    def read_table_data(self, transaction: dict, driver: object):
        driver.get(transaction['report_link'])
        time.sleep(2)
        politician_name = self.parse_politician_name(transaction['name'])
        politician = Politician.find_by_name_senate(politician_name, cursor)
        self.process_table_data(driver, politician)

    def parse_politician_name(self, name:str):
        name_split = name.split(' ')
        if len(name_split) > 2:
            full_name = ' '.join([name_split[0], name_split[-1]])
            return full_name
        return name

    def process_table_data(self, driver: object, politician: Politician):
        try:
            driver.find_element(By.XPATH, '//*[@id="content"]/div/div/section/div/div/table/tbody')
            rows = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='content']/div/div/section/div/div/table/tbody/tr")))
            for row in rows:
                cols = row.find_elements(By.TAG_NAME,'td')
                text = [col.text for col in cols]
                self.check_for_matching_ticker(text, politician)
        except Exception as error:
            print('Record could not be added to database', error)

    def format_database_values(self, stock: Stock, text: list, politician: Politician):
        transaction_date = text[1]
        purchase_or_sold = text[6]
        amount = text[7]
        return [stock.id, politician.id, purchase_or_sold, transaction_date, amount]
    
    def check_for_matching_ticker(self, text, politician):
        stock = Stock.find_by_stock_marker(text[3], cursor)
        if not stock:
            self.create_asset_values(text, politician)
        else:
            values = self.format_database_values(stock, text, politician)
            add_record_to_database(values, USER, DATABASE)

    def format_asset_name(self, text):
        try:
            name = text[4].split('\n')[0]
            return name
        except:
            return text[4]
    
    def create_asset_values(self, text, politician):
        name = self.format_asset_name(text)
        type = text[5]
        add_asset_record([name, type], USER, DATABASE)
        asset = Stock.find_by_company_name(name, cursor)
        values = self.format_database_values(asset[0], text, politician)
        add_record_to_database(values, USER, DATABASE)

    
         

