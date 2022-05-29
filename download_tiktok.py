import os
import time
import logging
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info("Start working")

options = webdriver.ChromeOptions()
# Version: https://portableapps.com/apps/internet/google_chrome_portable
options.binary_location = "GoogleChromePortable\\App\\Chrome-bin\\chrome.exe"
options.add_argument('headless');
options.add_experimental_option("prefs", {
    "download.default_directory": f"{os.getcwd()}\\files",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# Version: https://chromedriver.storage.googleapis.com/index.html?path=100.0.4896.60/
chrome_driver_binary = "chromedriver.exe"

driver = webdriver.Chrome(chrome_driver_binary, options=options)

with open("urls.txt") as file:
    url_lists = file.readlines()

for url in url_lists:
    try:
        driver.get("https://godownloader.com/en")

        elem = driver.find_elements(By.TAG_NAME, "input")[0]
        elem.clear()
        elem.send_keys(url)

        driver.implicitly_wait(10)
        elem = driver.find_element(By.XPATH, '//button[text()="Download Now"]')
        elem.click()

        driver.implicitly_wait(1)
        #if driver.find_element(By.XPATH, "//*[contains(text(), 'Please enter a valid URL')]").is_displayed():
        if len(driver.find_elements(By.XPATH, '//div[@role="alert"]')) > 0:
            logger.info(f"Invalid URL: {url}")
            continue

        driver.implicitly_wait(10)
        if "tiktok.com" in url:
            elem = driver.find_element(By.XPATH, '//button[text()="Download Video No Watermark (HD)"]')
        #elif "instagram.com" in url:
        #    driver.implicitly_wait(30)
        #    elem = driver.find_element(By.XPATH, '//button[text()="Download Video Best Quality"]')
        else:
            logger.info(f"Invalid URL: {url}")
            continue
        elem.click()
        logger.info(f"Downloading {url}")
    except Exception as e:
        logging.error(traceback.format_exc())
        continue

    time.sleep(5)

logger.info("All TikToks downloaded")

time.sleep(10)
driver.close()