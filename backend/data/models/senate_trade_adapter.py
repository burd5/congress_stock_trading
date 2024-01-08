from api.models.politician import Politician
from api.models.stock import Stock
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from settings import USER, DATABASE
from api.lib.db import cursor, add_record_to_database, check_record_existence
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
            table_data = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/section/div/div/table/tbody')
            rows = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='content']/div/div/section/div/div/table/tbody/tr")))
            for row in rows:
                cols = row.find_elements(By.TAG_NAME,'td')
                text = [col.text for col in cols]
                self.check_for_matching_ticker(text, politician)
        except:
            print('image_based_file')

    def format_database_values(self, stock: Stock, text: list, politician: Politician):
        transaction_date = text[1]
        purchase_or_sold = text[6]
        amount = text[7]
        return [stock.id, politician.id, purchase_or_sold, transaction_date, amount]
    
    def check_for_matching_ticker(self, text, politician):
        stock = Stock.find_by_stock_marker(text[3], cursor)
        if stock: 
            values = self.format_database_values(stock, text, politician)
            add_record_to_database(values, USER, DATABASE)


"""
{'name': 'Lamar Alexander', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/bae84d14-c80e-424f-9a21-241c0c47eacc/'}, {'name': 'Lamar Alexander', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/be49e822-6d8a-43d4-9f17-41f6e6806786/'}, {'name': 'Lamar Alexander', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/d383f953-1e1c-4557-9d1e-5c5dd0f2fbfa/'}, {'name': 'Lamar Alexander', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/a5816e0d-05f2-4db3-824d-d7e8c10758af/'}, {'name': 'Lamar Alexander', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/e4a2aa00-e5bc-4c2f-967a-ff0b5bb5089b/'}, {'name': 'Lamar Alexander', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/8db16cde-8a14-4ea2-92ed-71d7f73ad131/'}, {'name': 'Lamar Alexander', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/288c9d97-88cf-42f7-8736-661d3a564ef7/'}, {'name': 'Lamar Alexander', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/86e969b3-64e7-4a51-84d7-da82847b501e/'}, {'name': 'Lamar Alexander', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/0b0bd265-2339-4099-830f-8b4dbc860e26/'}, {'name': 'Lamar Alexander', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/b0d7fbcc-0fb9-4b35-8f0f-0ab2f58e781e/'}, {'name': 'Lamar Alexander', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/f2e9b6f6-de9a-4d30-8fb0-78e0e45fd1f2/'}, {'name': 'Lamar Alexander', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/3ace556d-de83-4080-98f1-7848fecf7f70/'}, {'name': 'Lamar Alexander', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/2fe6b2b0-a472-428d-bbe7-e20d2d1d2d48/'}, {'name': 'Lamar Alexander', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/05f5d46b-c3b0-4ef3-aaa6-a1f49574b5af/'}, {'name': 'Lamar Alexander', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/61380aec-bd2b-4331-bc7c-bf00e7438280/'}, {'name': 'Lamar Alexander', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/a5ea65ef-3943-4944-b192-988ab6adaa21/'}, {'name': 'John A Barrasso', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/265964e0-3d22-4a52-af4f-37916b56390d/'}, {'name': 'Michael F Bennet', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/cd2add48-f2bc-42bc-acbd-d8f7b502eae1/'}, {'name': 'Michael F Bennet', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/d72b5a11-2578-4923-b5db-120464bc4261/'}, {'name': 'Michael F Bennet', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/3d1b3c85-7b41-4183-89d6-aec3600db2a1/'}, {'name': 'Michael F Bennet', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/cc21478c-7266-432d-9412-efd04d059ab4/'}, {'name': 'Michael F Bennet', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/f590a331-1f74-4d08-b79f-88930593f314/'}, {'name': 'Michael F Bennet', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/ca3a419d-76cb-45f4-b6ac-203baf908371/'}, {'name': 'Michael F Bennet', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/596ec5e5-2392-4cb7-a12d-8466ab2a4f8e/'}, {'name': 'Michael F Bennet', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/d4ab53a8-86b8-43ee-8d12-64458b870046/'}, {'name': 'Michael F Bennet', 'report_link': 'https://efdsearch.senate.gov/search/view/ptr/596ec5e5-2392-4cb7-a12d-8466ab2a4f8e/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/70abcb59-ae68-44bc-a8db-7ccc5673c5af/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/a84b299c-20ca-4f6d-8987-a23c5f5bcf54/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/7f33e550-caa2-4718-8bf5-d73d0adb010b/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/03b9dc2b-2e00-44ed-8b2f-cfc729313f92/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/b7efa216-68b7-412b-9ca9-a491afc231ff/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/4fced9a8-70f9-4a26-bd65-f4537ccb4a09/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/3958238C-743E-4223-AFB0-CDB74F59BA96/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/c3471d47-b8ef-4f81-95a4-296a440b2ddc/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/b592b168-6ec8-4ea4-b153-cd3148404c2e/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/8e223aef-2f07-43cb-9af3-12914429aa46/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/573468dc-d6e1-4873-a3e8-cfbb9f3bb958/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/A701D31F-B3B0-483E-8F38-729D0A97BA86/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/e27fd07d-ed8f-4d3e-b825-81e9bfceda1f/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/b3ad2c88-ec0f-490b-bfca-7d3d127f78ee/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/bcf4205f-7df0-48c9-b51e-25c5b99b2bd2/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/BAB946BE-A931-4A1D-ACE4-6DBEA29A445C/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/39aa7199-9987-407f-8d8e-2ed7a49d0339/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/40f35e56-632b-4b9d-b28c-658419ca0d53/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/5222f3bf-d740-4457-b3b9-190e56485109/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/53a76d97-d1c7-4c80-999a-99d12987979b/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/e218c064-9915-4e51-9c4b-38065c6f822b/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/19d089ab-729e-4b52-95c4-585a9b085b55/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/e24251ff-2099-453b-9578-470590cb971f/'}, {'name': 'RICHARD BLUMENTHAL', 'report_link': 'https://efdsearch.senate.gov/search/view/paper/7f733a14-a6be-4cc1-af27-c4f059fedb3f/'}
"""