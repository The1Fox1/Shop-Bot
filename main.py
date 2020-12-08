from scrapy.crawler import CrawlerProcess
from shopbot.spiders import bestbuybot
import logging

# Set up logging
logging.basicConfig(
    filename='bot.log',
    format='%(asctime)s  %(levelname)s :: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("ShopBot")

# Set Up Process
logger.info("Set up ShopBot")
process = CrawlerProcess()
process.crawl(bestbuybot.BestbuySpider)
# process.crawl(neweggbot.NeweggSpider)

# RUN
logger.info("Starting ShopBot")
process.start()  # the script will block here until all crawling jobs are finished
logger.info("ShopBot Finished..........")
