import logging
import socket
from selenium import webdriver

from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class SpiderHelper:
    @staticmethod
    def get_product_name(s):
        if "RTX" in s.upper():
            if "3080" in s:
                return "RTX 3080"
            elif "3070" in s:
                return "RTX 3070"
            elif "3060" in s:
                return "RTX 3060"
            else:
                return "Unkown Nvidia RTX"
        elif "RYZEN" in s:
            if "5900" in s:
                return "Ryzen 9 5900x"
            elif "5800" in s:
                return "Ryzen 7 5800x"
            elif "5600" in s:
                return "Ryzen 5 5600x"
            else:
                return "Unknown AMD Ryzen"
        return "Unkown"

    @staticmethod
    def default_user_agent():
        return "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) " \
                "Chrome/43.0.2357.130 Safari/537.36 "

    @staticmethod
    def get_logger(name):
        log = logging.getLogger(name)
        handler = logging.FileHandler("bot.log")
        handler.setFormatter(logging.Formatter('%(asctime)s  %(levelname)s :: %(message)s'))
        log.addHandler(handler)
        log.setLevel(logging.INFO)
        return log

    @staticmethod
    def get_driver():
        deviceName = socket.gethostname()
        profilePath = r"C:\Users\brand\AppData\Roaming\Mozilla\Firefox\Profiles"
        profilePath += r"\oy8a68ov.default" if ("DELTA" not in deviceName.upper()) else r"\hwhwzqvw.default"
        driverPath = "C:" if ("DELTA" not in deviceName.upper()) else "G:"
        driverPath += r'\Users\brand\webdrivers\geckodriver.exe'

        # options = webdriver.ChromeOptions()
        # options.add_argument(r'user-data-dir=C:\Users\brand\AppData\Local\Google\Chrome\User Data')
        # driver = webdriver.Chrome(chrome_options=options, executable_path=r'G:\Users\brand\webdrivers\chromedriver.exe')

        profile = webdriver.FirefoxProfile(profilePath)
        return webdriver.Firefox(firefox_profile=profile, executable_path=driverPath)