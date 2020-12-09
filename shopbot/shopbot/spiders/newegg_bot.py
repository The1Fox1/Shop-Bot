import scrapy
import time
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .spider_helper import SpiderHelper

# Set up logging
log = SpiderHelper.get_logger(name="Newegg")

# Definition
class NeweggSpider(scrapy.Spider):
   name = "newegg"
   USER_AGENT = SpiderHelper.default_user_agent()
   # Enter Your Product URL Here.
   start_urls = ["https://www.newegg.com/unitek-y-p527/p/0FB-02C2-00001?Item=9SIA2BPB8J5199&cm_sp=Dailydeal_SS-_-9SIA2BPB8J5199-_-12082020" #testURL
                #"https://www.newegg.com/amd-ryzen-5-5600x/p/N82E16819113666?Item=N82E16819113666&Tpk=19-113-666",
                # "https://www.newegg.com/amd-ryzen-7-5800x/p/N82E16819113665",
                 #"https://www.newegg.com/amd-ryzen-9-5900x/p/N82E16819113664",
                 #"https://www.newegg.com/asus-geforce-rtx-3070-ko-rtx3070-o8g-gamin/p/N82E16814126466",
                 #"https://www.newegg.com/asus-geforce-rtx-3080-tuf-rtx3080-o10g-gaming/p/N82E16814126452"
    ]

   def parse(self, response):
       # Finding Product Status From Scraping.
       try:
           productName = SpiderHelper.get_product_name(response.request.url)
           product = response.xpath(
               ".//*[@class='btn btn-primary btn-wide']")
           if product:
               log.warning(f"{productName} is Currently: Available.")
           else:
               log.info(f"{productName} is Out of Stock.")
       except NoSuchElementException:
           log.error(NoSuchElementException)
           pass

       # Start selenium driver
       if product:
           log.info(f"Found {productName} to add to cart.")

           # Booting WebDriver.
           driver = SpiderHelper.get_driver()

           # Starting Webpage.
           driver.get(response.url)
           time.sleep(3)

           # Click Add to Cart.
           log.info("Clicking Add To Cart Button.")
           driver.find_element_by_xpath(
               ".//*[@class='btn btn-primary btn-wide']").click()
           time.sleep(5)

           # Click Cart.
           log.info("Going to Shopping Cart.")
           driver.get("https://secure.newegg.com/shop/cart")
           time.sleep(5)

           # Click Check-out Button.
           log.info("Clicking Checkout Button.")
           driver.find_element_by_xpath(".//*[@class='btn btn-primary btn-wide']").click()

           # Giving Website Time To Login.
           log.info("Giving Website Time To Login..")
           wait = WebDriverWait(driver, 10)
           wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='signInSubmit']")))
           time.sleep(3)

           # ARE YOU READY TO BUY?
           log.info(f"Buying {productName}.")
           # Click past Shipping
           driver.find_elements_by_xpath(".//*[@class='btn btn-primary checkout-step-action-done layout-quarter']")[0].click()
           # Click past delivery
           driver.find_elements_by_xpath(".//*[@class='btn btn-primary checkout-step-action-done layout-quarter']")[1].click()

           log.info("Bot has Completed Checkout.")
           time.sleep(18000)

       else:
           log.info("Retrying Bot In 15 Seconds.")
           time.sleep(15)
           yield Request(url=response.url, callback=self.parse, dont_filter=True)

