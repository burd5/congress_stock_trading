from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
soup = BeautifulSoup('html', 'lxml')


class SenateScraper:
    def __init__(self):
        self.transaction_reports = []
    
    def initialize_webscrape(self):
        driver = webdriver.Chrome()
        self.go_to_search_table(driver)
        driver.quit()
        return self.transaction_reports

    def go_to_search_table(self, driver: object):
        driver.get('https://efdsearch.senate.gov/search/')
        self.select_report_type_and_date(driver)

    def select_report_type_and_date(self, driver: object):
        search_button = driver.find_element(By.XPATH, '//*[@id="agree_statement"]')
        search_button.click()
        time.sleep(2)
        search_button = driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div/div[5]/div/form/fieldset[3]/div/div/div/div[1]/div[2]/label/input')
        search_button.click()
        time.sleep(2)
        self.select_from_date(driver)

    def select_from_date(self, driver: object):
        search_button = driver.find_element(By.XPATH, '//*[@id="fromDate"]')
        search_button.click()
        time.sleep(2)
        search_button = driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/select[1]/option[1]')
        search_button.click()
        time.sleep(2)
        search_button = driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[2]/a')
        search_button.click()
        time.sleep(2)
        self.select_to_date(driver)

    def select_to_date(self, driver: object):
        search_button = driver.find_element(By.XPATH, '//*[@id="toDate"]')
        search_button.click()
        time.sleep(2)
        search_button = driver.find_element(By.CSS_SELECTOR, '.ui-state-default.ui-state-highlight')
        search_button.click()
        time.sleep(2)
        search_button = driver.find_element(By.XPATH, '//*[@id="searchForm"]/div/button')
        search_button.click()
        time.sleep(2)
        find_last_number = driver.find_element(By.XPATH, '//*[@id="filedReports_paginate"]/span/a[last()]')
        page_number = int(find_last_number.text) + 1
        self.find_table_information_for_page_range(driver, page_number)

    def find_table_information_for_page_range(self, driver: object, page_number:int):
        for page in range(1, page_number):
            rows = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='filedReports']/tbody/tr")))
            time.sleep(2)
            self.find_column_information_for_current_table(rows)
            next = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//*[@id='filedReports_next']")))
            next.click() 
            time.sleep(2)

    def find_column_information_for_current_table(self, rows: list):
        for row in rows:
            cols = row.find_elements(By.TAG_NAME,'td')
            transaction_report = self.add_record_to_dict_if_match(cols)
            if transaction_report:
                self.transaction_reports.append(transaction_report)

    def add_record_to_dict_if_match(self, cols: list):
        name = cols[0].text + ' ' + cols[1].text
        link_element = cols[3]
        anchor_tag = link_element.find_element(By.TAG_NAME, 'a')
        href = anchor_tag.get_attribute('href')
        return {'name': name, 'report_link': href}
    
