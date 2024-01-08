from bs4 import BeautifulSoup
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from io import StringIO


def find_today():
  today = datetime.datetime.now()
  return today

def scraping_process_begin():
    driver = driver_initiate()
    today = find_today()
    return driver, today

def driver_initiate():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    #chrome_options.headless = headless
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(3)
    url = 'https://www.zvg-portal.de/index.php?button=Termine%20suchen'
    driver.get(url)
    text_to_check = "Zwangsversteigerungstermine"
    element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "body")))
    if text_to_check in element.text:
        print("Page loaded.")
    else:
        print("Page not loaded.")
    return driver

def find_field_selection(driver, css_name, option):
    element = driver.find_element(By.NAME, css_name)
    field_text = element.text
    options = field_text.split('\n')
    index = options.index(option)
    select_element = Select(element)
    select_element.select_by_index(index)
    return None

def initial_selection():
    start_process = scraping_process_begin()
    driver = start_process[0]
    fields = {
        'land': 'land_abk',
        'gericht': 'ger_id'
    }
    find_field_selection(driver, 'land_abk', 'Bayern')
    find_field_selection(driver, 'ger_id', 'Traunstein')
    submit = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/form/h3/nobr/button[1]")
    submit.click()
    return driver

def stract_table():
    driver = initial_selection()
    pages = driver.find_element(By.XPATH, "//*[@id='inhalt']/form/table")
    pages_links = pages.find_elements(By.TAG_NAME, "a")
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, "html.parser", from_encoding="windows-1252")
    tables = soup.find_all("table")
    html_string = str(tables[0])
    df = pd.read_html(StringIO(html_string))[0]
    import ipdb; ipdb.set_trace(context=10)

if __name__ == '__main__':
    stract_table()
