import scrapy
import time
from selenium import webdriver
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging

# Set up logging
log = logging.getLogger("Best Buy")

def getproductname(s):
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

class BestbuySpider(scrapy.Spider):
   name = "bestbuy"
   USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) " \
                "Chrome/43.0.2357.130 Safari/537.36 "
   # Enter Your Product URL Here.
   start_urls = [
       "https://www.bestbuy.com/site/amd-ryzen-5-3600x-3rd-generation-6-core-12-thread-3-8-ghz-4-4-ghz-max-boost-socket-am4-unlocked-desktop-processor/6356644.p?skuId=6356644" #TEST URL
        "https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440",
        "https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442",
        "https://www.bestbuy.com/site/nvidia-geforce-rtx-3060-ti-8gb-gddr6-pci-express-4-0-graphics-card-steel-and-black/6439402.p?skuId=6439402",
        "https://www.bestbuy.com/site/amd-ryzen-9-5900x-4th-gen-12-core-24-threads-unlocked-desktop-processor-without-cooler/6438942.p?skuId=6438942",
        "https://www.bestbuy.com/site/amd-ryzen-7-5800x-4th-gen-8-core-16-threads-unlocked-desktop-processor-without-cooler/6439000.p?skuId=6439000",
        "https://www.bestbuy.com/site/amd-ryzen-5-5600x-4th-gen-6-core-12-threads-unlocked-desktop-processor-with-wraith-stealth-cooler/6438943.p?skuId=6438943",
   ]

   def parse(self, response):

       # Finding Product Status.
       try:
           productName = getproductname(response.request.url)
           product = response.xpath(
               "//*[@class='btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button']")
           if product:
               log.warning(f"{productName} is Currently: Available.")
           else:
               log.info(f"{productName} is Out of Stock.")
       except NoSuchElementException:
           pass

       if product:
           log.info(f"Found 1 {productName} to add to cart.")

           # Booting WebDriver.
           profile = webdriver.ChromeOptions(r'C:\Users\bran\AppData\Local\Google\Chrome\User Data\Default')
           driver = webdriver.Chrome(options=profile, executable_path='C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')

           # Starting Webpage.
           driver.get(response.url)
           time.sleep(3)

           # Click Add to Cart.
           log.info("Clicking Add To Cart Button.")
           driver.find_element_by_xpath(
               "//*[@class='btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button']").click()
           time.sleep(3)

           # Click Cart.
           log.info("Going to Shopping Cart.")
           driver.get("https://www.bestbuy.com/cart")
           time.sleep(5)

           # Click Check-out Button.
           log.info("Clicking Checkout Button.")
           driver.find_element_by_xpath("//*[@class='btn btn-lg btn-block btn-primary']").click()

           # Giving Website Time To Login.
           log.info("Giving Website Time To Login..")
           wait = WebDriverWait(driver, 20)
           wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='btn btn-lg btn-block btn-primary button__fast-track']")))
           time.sleep(3)

           # CVV Number Input.
           log.info("Inputing CVV Number.")
           try:
               security_code = driver.find_element_by_id("credit-card-cvv")
               time.sleep(5)
               security_code.send_keys("009")  # You can enter your CVV number here.
           except NoSuchElementException:
               pass

           # ARE YOU READY TO BUY?
           log.info(f"Buying {productName}.")
           driver.find_element_by_xpath("//*[@class='btn btn-lg btn-block btn-primary button__fast-track']").click()

           log.info("Bot has Completed Checkout.")
           time.sleep(18000)

       else:
           log.info("Retrying Bot In 15 Seconds.")
           time.sleep(15)
           yield Request(response.url, callback=self.parse, dont_filter=True)

