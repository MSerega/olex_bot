import os
import time

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


async def get_alert():
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

        size = capabilities = {
            "resolution": "1366x768"
        }

        with webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                              desired_capabilities=size,
                              options=options) as driver:
            url = 'http://alerts.in.ua'
            auto_map = os.path.abspath("/olex_bot/images/alarms/map.png")
            driver.get(url)
            time.sleep(5)
            driver.save_screenshot(auto_map)
            time.sleep(4)
            driver.close()
    except WebDriverException as e:
        return f"Виникла помилка. Спробуйте виконати команду ще раз."

