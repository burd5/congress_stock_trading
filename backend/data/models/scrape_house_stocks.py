from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
soup = BeautifulSoup('html', 'lxml')

class HouseScraper:
    def __init__(self):
        self.transaction_reports = []

    def initialize_webscrape(self, year_identifier, end_page):
        driver = webdriver.Chrome()
        self.go_to_search_table(driver, year_identifier, end_page)
        driver.quit()
        return self.transaction_reports

    def go_to_search_table(self,driver, year_identifier, end_page):
        driver.get('https://disclosures-clerk.house.gov/FinancialDisclosure')
        self.go_to_requested_filing_year(driver, year_identifier)
        time.sleep(3)
        self.find_table_information_for_page_range(1, end_page, driver)

    def go_to_requested_filing_year(self,driver,year_identifier):
        search_button = driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div[1]/ul/li[7]/a')
        search_button.click()
        time.sleep(2)
        dropdown = driver.find_element(By.XPATH, f'//*[@id="FilingYear"]/option[{year_identifier}]')
        dropdown.click()
        time.sleep(2)
        search_click = driver.find_element(By.XPATH, '//*[@id="search-members"]/form/div[4]/button[1]')
        search_click.click()
        time.sleep(3)

    def find_table_information_for_page_range(self,start, stop, driver):
        for page in range(start, stop + 1):
            element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//a[text()={page}]")))
            element.click()
            time.sleep(2)
            rows = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr"))) 
            self.find_column_information_for_current_table(rows)
    
    def find_column_information_for_current_table(self,rows):
        for row in rows:
            cols = row.find_elements(By.TAG_NAME,'td')
            transaction_report = self.add_record_to_dict_if_match(cols)
            if transaction_report:
                self.transaction_reports.append(transaction_report)

    def add_record_to_dict_if_match(self,cols):
        name = cols[0].text
        office = cols[1].text
        filing_year = cols[2].text
        href = self.check_if_report_is_public_transaction_record(cols)
        if href:
            return {'name': name, 'office': office, 'filing_year': filing_year, 'report_link': href}
            
    def check_if_report_is_public_transaction_record(self,cols):
        if cols[3].text == 'PTR Original':
            link_element = cols[0]
            anchor_tag = link_element.find_element(By.TAG_NAME, 'a')
            href = anchor_tag.get_attribute('href') 
            return href
