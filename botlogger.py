import logging

# Set up logging
logging.basicConfig(
    filename='bot.log',
    format='%(asctime) [%(levelname)s] :: %(message)s',
    level=logging.INFO
)
logging.getLogger("ShopBot")

# definition


def info(message, servicename=''):
    logging.info(f'[{servicename}]: {message}')


def warn(message, servicename=''):
    logging.warning(f'[{servicename}]: {message}')


def error(message, servicename = ''):
    logging.error(f'[{servicename}]: {message}')
