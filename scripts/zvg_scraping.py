import datetime
from selenium.webdriver.chrome.options import Options
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
    driver.get('https://www.zvg-portal.de/index.php?button=Termine%20suchen')
    return driver

if __name__ == '__main__':
    scraping_process_begin()
