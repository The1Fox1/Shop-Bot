import scrapy
import time
from selenium import webdriver
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .spider_helper import SpiderHelper
import socket

# Set up logging
log = SpiderHelper.get_logger(name="Best Buy")

# Definition
class BestbuySpider(scrapy.Spider):
   name = "bestbuy"
   USER_AGENT = SpiderHelper.default_user_agent()
   # Enter Your Product URL Here.
   start_urls = [
       "https://www.bestbuy.com/site/marvels-spider-man-miles-morales-standard-launch-edition-playstation-5/6430146.p?skuId=6430146" #TEST URL
        #"https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440",
        #"https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442",
        #"https://www.bestbuy.com/site/nvidia-geforce-rtx-3060-ti-8gb-gddr6-pci-express-4-0-graphics-card-steel-and-black/6439402.p?skuId=6439402",
        #"https://www.bestbuy.com/site/amd-ryzen-9-5900x-4th-gen-12-core-24-threads-unlocked-desktop-processor-without-cooler/6438942.p?skuId=6438942",
        #"https://www.bestbuy.com/site/amd-ryzen-7-5800x-4th-gen-8-core-16-threads-unlocked-desktop-processor-without-cooler/6439000.p?skuId=6439000",
        #"https://www.bestbuy.com/site/amd-ryzen-5-5600x-4th-gen-6-core-12-threads-unlocked-desktop-processor-with-wraith-stealth-cooler/6438943.p?skuId=6438943",
   ]

   def parse(self, response):
       # Finding Product Status.
       try:
           deviceName = socket.gethostname() # Grab device name to determine directory settings
           productName = SpiderHelper.get_product_name(response.request.url)
           product = response.xpath(
               "//*[@class='btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button']")
           if product:
               log.warning(f"{productName} is Currently: Available.")
           else:
               log.info(f"{productName} is Out of Stock.")
       except NoSuchElementException:
           log.error(NoSuchElementException)
           pass

       if product:
           log.info(f"Found {productName} to add to cart.")

           # Booting WebDriver
           driver = SpiderHelper.get_driver()
           wait = WebDriverWait(driver, 15)

           # Starting Webpage.
           driver.get(response.url)
           wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'add-to-cart-button') and contains(@class, 'btn-primary')]")))

           # Click Add to Cart.
           log.info("Clicking Add To Cart Button.")
           wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'add-to-cart-button') and contains(@class, 'btn-primary')]")))
           driver.find_element_by_xpath("//button[contains(@class,'add-to-cart-button') and contains(@class, 'btn-primary')]").click()
           time.sleep(1)

           # Go to Cart.
           log.info("Going to Shopping Cart.")
           driver.get("https://www.bestbuy.com/cart")
           time.sleep(2)

           # Click Check-out Button.
           log.info("Clicking Checkout Button.")
           driver.find_element_by_xpath("//*[@class='btn btn-lg btn-block btn-primary']").click()

           # Login.
           wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'btn btn-secondary btn-lg')]")))
           if len(driver.find_elements_by_id('fld-e')) != 0:
                driver.find_element_by_id('fld-e').send_keys("brandonslyfox@gmail.com")
           driver.find_element_by_id('fld-p1').send_keys("CalvinandHobbes1!")
           driver.find_element_by_xpath(".//button[contains(@class,'btn btn-secondary btn-lg')]").click()
           time.sleep(5)

            # Fill Shipping info
           if len(driver.find_elements_by_id('consolidatedAddresses.ui_address_2.firstName')) != 0:
               driver.find_element_by_id('consolidatedAddresses.ui_address_2.firstName').send_keys('Brandon')
               driver.find_element_by_id('consolidatedAddresses.ui_address_2.lastName').send_keys('Fox')
               driver.find_element_by_id('consolidatedAddresses.ui_address_2.street').send_keys('16168 Alcima Ave')
               driver.find_element_by_id('consolidatedAddresses.ui_address_2.city').send_keys('Pacific Palisades')
               driver.find_element_by_id('consolidatedAddresses.ui_address_2.zipcode').send_keys('90272')
               statedropdown = Select(driver.find_elements_by_id("payment.billingAddress.state"))
               statedropdown.select_by_visible_text("CA");
               if driver.find_element_by_id('save-for-billing-address-ui_address_2').is_selected():
                driver.find_element_by_id('save-for-billing-address-ui_address_2').click()

           wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@class='btn btn-lg btn-block btn-secondary']")))
           driver.find_element_by_xpath(".//*[@class='btn btn-lg btn-block btn-secondary']").click()

            # Fill billing info
           wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='optimized-cc-card-number']")))
           driver.find_element_by_id('optimized-cc-card-number').send_keys("4266841630631644")

           wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='credit-card-cvv']")))
           driver.find_element_by_id('credit-card-cvv').send_keys("009")

           expmonthdropdown = Select(driver.find_elements_by_xpath("//*[@class='c-dropdown v-medium c-dropdown v-medium smart-select']")[0])
           expmonthdropdown.select_by_visible_text("04")
           expyeardropdown = Select(driver.find_elements_by_xpath("//*[@class='c-dropdown v-medium c-dropdown v-medium smart-select']")[1])
           expyeardropdown.select_by_visible_text("2024")

           if len(driver.find_elements_by_id('payment.billingAddress.firstName')) != 0:
               driver.find_element_by_id('payment.billingAddress.firstName').send_keys('Brandon')
               driver.find_element_by_id('payment.billingAddress.lastName').send_keys('Fox')
               driver.find_element_by_id('payment.billingAddress.street').send_keys('783 Gatun st')
               driver.find_element_by_id('payment.billingAddress.city').send_keys('San Pedro')
               driver.find_element_by_id('payment.billingAddress.zipcode').send_keys('90731')
               billstatedropdown = Select(driver.find_element_by_id("payment.billingAddress.state"))
               billstatedropdown.select_by_visible_text("CA")

           # ARE YOU READY TO BUY?
           #log.info(f"Buying {productName}.")
           #driver.find_element_by_xpath("//*[@class='btn btn-lg btn-block btn-primary button__fast-track']").click()

           log.info("Bot has Readied checkout")
           time.sleep(180000)

       else:
           log.info("Retrying Bot In 15 Seconds.")
           time.sleep(15)
           yield Request(url=response.url, callback=self.parse, dont_filter=True)

