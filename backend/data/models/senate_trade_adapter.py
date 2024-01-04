from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
soup = BeautifulSoup('html', 'lxml')

class ReadTransactionTableData:
    def process_transactions(self, transactions: list):
        driver = self.bypass_agree_statement()
        for transaction in transactions:
            self.read_table_data(transaction, driver)

    def bypass_agree_statement(self):
        driver = webdriver.Chrome()
        driver.get('https://efdsearch.senate.gov/search/')
        search_button = driver.find_element(By.XPATH, '//*[@id="agree_statement"]')
        search_button.click()
        time.sleep(2)
        return driver

    def read_table_data(self, transaction: dict, driver):
        driver.get(transaction['report_link'])
        self.process_table_data(driver)
        driver.quit()

    def process_table_data(self, driver: object):
        try:
            table_data = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/section/div/div/table/tbody')
            rows = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='content']/div/div/section/div/div/table/tbody/tr")))
            for row in rows:
                cols = row.find_elements(By.TAG_NAME,'td')
                text = [col.text for col in cols]
        except:
            print('image_based_file')
