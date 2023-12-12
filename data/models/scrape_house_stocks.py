from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
soup = BeautifulSoup('html', 'lxml')

transaction_reports = []

def initialize_webscrape():
    driver = webdriver.Chrome()
    go_to_search_table(driver)
    driver.quit()

def go_to_search_table(driver):
    driver.get('https://disclosures-clerk.house.gov/FinancialDisclosure')
    go_to_requested_filing_year(driver)
    time.sleep(3)
    find_table_information_for_page_range(1,5, driver)

def go_to_requested_filing_year(driver):
    search_button = driver.find_element(By.XPATH, '//*[@id="main-content"]/div/div[1]/ul/li[7]/a')
    search_button.click()
    time.sleep(2)
    dropdown = driver.find_element(By.XPATH, '//*[@id="FilingYear"]/option[12]')
    dropdown.click()
    time.sleep(2)
    search_click = driver.find_element(By.XPATH, '//*[@id="search-members"]/form/div[4]/button[1]')
    search_click.click()
    time.sleep(3)

def find_table_information_for_page_range(start, stop, driver):
    for page in range(start, stop + 1):
        element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//a[text()={page}]")))
        element.click()
        time.sleep(2)
        rows = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr"))) 
        find_column_information_for_current_table(rows)
   
def find_column_information_for_current_table(rows):
    for row in rows:
        cols = row.find_elements(By.TAG_NAME,'td')
        transaction_report = add_record_to_dict_if_match(cols)
        if transaction_report:
            transaction_reports.append(transaction_report)

def add_record_to_dict_if_match(cols):
    name = cols[0].text
    office = cols[1].text
    filing_year = cols[2].text
    href = check_if_report_is_public_transaction_record(cols)
    if href:
        return {'name': name, 'office': office, 'filing_year': filing_year, 'report_link': href}
        
def check_if_report_is_public_transaction_record(cols):
    if cols[3].text == 'PTR Original':
        link_element = cols[0]
        anchor_tag = link_element.find_element(By.TAG_NAME, 'a')
        href = anchor_tag.get_attribute('href') 
        return href
