import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver


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


if __name__ == '__main__':
    scraping_process_begin()
