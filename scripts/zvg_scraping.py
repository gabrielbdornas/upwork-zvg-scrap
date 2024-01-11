from bs4 import BeautifulSoup
import datetime
import os
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from io import StringIO


def find_today():
  today = datetime.datetime.now()
  return today.strftime("%Y%m%d")

def scraping_process_begin():
    driver = driver_initiate()
    return driver

def driver_initiate():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    # page_load = False
    url = 'https://www.zvg-portal.de/index.php?button=Termine%20suchen'
    # while not page_load:
    while True:
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.implicitly_wait(3)
            driver.set_page_load_timeout(5)
            driver.get(url)
            text_to_check = "Zwangsversteigerungstermine"
            element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body")))
            if text_to_check in element.text:
                print("Page loaded.")
            else:
                print("Page loaded but something went wrong with it.")
            # page_load = True
            break
        except TimeoutException:
            print("Page load timeout. Retrying...")
            driver.quit()
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
    driver = start_process
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
    soup = BeautifulSoup(html_content, "html.parser")
    tables = soup.find_all("table")
    html_string = str(tables[0])
    df = pd.read_html(StringIO(html_string))[0]
    salve_csv(df)
    return None

def salve_csv(df):
    today = find_today()
    if not os.path.exists(f'data/{today}'):
        os.mkdir(f'data/{today}')
    aktenzeichen = list(df[1][df[0] == 'Aktenzeichen'])
    objekt_lage = list(df[1][df[0] == 'Objekt/Lage'])
    data = {
        'aktenzeichen': aktenzeichen,
        'objekt_lage': objekt_lage
    }
    new_df = pd.DataFrame(data)
    new_df.index.name = 'id'
    new_df.to_csv(f'data/{today}/zvgs_crap.csv')
    return None

if __name__ == '__main__':
    stract_table()
    # import ipdb; ipdb.set_trace(context=10)
