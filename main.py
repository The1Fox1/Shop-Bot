from scrapy.crawler import CrawlerProcess
from shopbot.shopbot.spiders import bestbuy_bot, newegg_bot
import logging

# Set up logging
logger = logging.getLogger("Shop-Bot")
handler = logging.FileHandler("app.log")
handler.setFormatter(logging.Formatter('%(asctime)s  %(levelname)s :: %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Set Up Process
logger.info("Set up Shop-Bot")
process = CrawlerProcess()
process.crawl(bestbuy_bot.BestbuySpider)
#process.crawl(newegg_bot.NeweggSpider)

# RUN
logger.info("Starting Shop-Bot")
process.start()  # the script will block here until all crawling jobs are finished
logger.info("Shop-Bot Exiting..........")
