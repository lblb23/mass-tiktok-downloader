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
#options.add_argument('headless');
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
        time.sleep(5)

        elem = driver.find_elements(By.TAG_NAME, "input")[0]
        elem.clear()
        elem.send_keys(url)

        time.sleep(5)

        if len(driver.find_elements(By.XPATH, '//a[contains(text(), "Video No Watermark")]')) == 0:
            elem = driver.find_element(By.XPATH, '//button[text()="Download Now"]')
            elem.click()

        time.sleep(5)

        if "tiktok.com" in url:
            elem = driver.find_element(By.XPATH, '//a[contains(text(), "Video No Watermark")]')
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

time.sleep(300)
driver.close()