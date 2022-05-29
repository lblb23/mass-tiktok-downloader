import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import dearpygui.dearpygui as dpg

def start_browser():
    options = webdriver.ChromeOptions()
    options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    options.add_experimental_option("prefs", {
        "download.default_directory": "C:\\Users\\nissa\\PycharmProjects\\tiktok-downloader\\files\\",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    chrome_driver_binary = "C:\\Users\\nissa\\Downloads\\chromedriver_win32\\chromedriver.exe"

    driver = webdriver.Chrome(chrome_driver_binary, options=options)
    return driver

def download_tiktok(driver, url):
    driver.get("https://godownloader.com/en")

    elem = driver.find_elements(By.TAG_NAME, "input")[0]
    elem.clear()
    elem.send_keys(url)

    driver.implicitly_wait(10)
    elem = driver.find_element(By.XPATH, '//button[text()="Download Now"]')
    elem.click()

    driver.implicitly_wait(10)
    elem = driver.find_element(By.XPATH, '//button[text()="Download Video No Watermark (HD)"]')
    elem.click()

def close_browser(driver):
    driver.close()

def button_callback(sender, app_data, user_data):
    dpg.configure_item("download_button", enabled=False)
    driver = user_data

    print(f"sender is: {sender}")
    print(f"app_data is: {app_data}")
    print(f"user_data is: {user_data}")
    print(dpg.get_value("url_list"))

    url_list = dpg.get_value("url_list").split('\n')
    for url in url_list:
        # Validate url
        dpg.log(f"Downloading {url}")

        download_tiktok(driver, url)
        dpg.log(f"Downloaded")
        # Check downloading

    dpg.configure_item("download_button", enabled=True)


if __name__ == '__main__':
    dpg.create_context()

    with dpg.window(label="TikTok Downloader"):
        # configuration set when button is created

        driver = start_browser()

        input_txt = dpg.add_input_text(
            label="List of TikTok URLs",
            default_value="Add your TikTok links here...",
            multiline=True,
            tag="url_list"
        )

        dpg.add_button(
            label="Download",
            width=300,
            callback=button_callback,
            user_data=driver,
            tag="download_button"
        )

        close_browser(driver)


    dpg.show_item_registry()

    dpg.create_viewport(title='Custom Title', width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
