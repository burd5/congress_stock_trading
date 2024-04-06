from backend.api.models.politician import Politician
from backend.api.models.stock import Stock
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from backend.api.lib.db import add_record_to_senate_trades, check_report_link_existence, add_report_record
soup = BeautifulSoup('html', 'lxml')
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')
options.add_argument('--headless')
options.add_argument('--disable-gpu')

class TransformSenateRecordsData:
    def process_transactions(self, transactions: list):
        driver = self.bypass_agree_statement()
        for transaction in transactions:
            if check_report_link_existence(transaction['report_link']): continue
            add_report_record(transaction['report_link'])
            self.read_table_data(transaction, driver)
        driver.quit()

    def bypass_agree_statement(self):
        driver = webdriver.Chrome(options=options)
        driver.get('https://efdsearch.senate.gov/search/')
        search_button = driver.find_element(By.XPATH, '//*[@id="agree_statement"]')
        search_button.click()
        time.sleep(2)
        return driver

    def read_table_data(self, transaction: dict, driver: object):
        driver.get(transaction['report_link'])
        time.sleep(2)
        politician_name = self.parse_politician_name(transaction['name'])
        self.process_table_data(driver, politician_name)

    def parse_politician_name(self, name:str):
        name_split = name.split(' ')
        if len(name_split) > 2:
            names = [name.replace(',', '') for name in name_split if name not in ['Jr', 'Jr.']]
            full_name = ' '.join([names[0], names[-1]])
            return full_name
        return name

    def process_table_data(self, driver: object, politician: str):
        try:
            driver.find_element(By.XPATH, '//*[@id="content"]/div/div/section/div/div/table/tbody')
            rows = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='content']/div/div/section/div/div/table/tbody/tr")))
            for row in rows:
                cols = row.find_elements(By.TAG_NAME,'td')
                text = [col.text for col in cols]
                text[0] = politician
                add_record_to_senate_trades(text)
        except Exception as error:
            print('Record could not be added to database', error)