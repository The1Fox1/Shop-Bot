from scrapy.crawler import CrawlerProcess
from shopbot.shopbot.spiders import bestbuy_bot, newegg_bot
import logging

# Set up logging
logging.basicConfig(
    filename='app.log',
    format='%(asctime)s  %(levelname)s :: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("Shop-Bot")

# Set Up Process
logger.info("Set up Shop-Bot")
process = CrawlerProcess()
#process.crawl(bestbuy_bot.BestbuySpider)
process.crawl(newegg_bot.NeweggSpider)

# RUN
logger.info("Starting Shop-Bot")
process.start()  # the script will block here until all crawling jobs are finished
logger.info("Shop-Bot Finished..........")
