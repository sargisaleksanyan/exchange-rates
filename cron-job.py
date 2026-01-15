import schedule
import time
import logging
from datetime import datetime

from src.db.db_handler import DatabaseHandler
from src.util.common_classes.exchange_company import ExchangeCompany
from src.website_scrapers.banks.index import frequent_banks_update, non_frequent_banks_update
from src.website_scrapers.exchange_business.index import frequent_currency_exchange_update, \
    non_frequent_currency_exchange_update

dbHandler = DatabaseHandler()

#logger = logging.getLogger(__name__)
logger = logging.getLogger()


def init_logger():
    logging.basicConfig(filename='logs/info.log', level=logging.INFO)


def update_company_exchange_data(company_exchange_data: ExchangeCompany):
    company = dbHandler.find_company_by_url(company_exchange_data.url)
    if company == None:
        dbHandler.insert_data(company_exchange_data)
    else:
        dbHandler.update_exchange_rate(company_exchange_data)
        # update


def init_non_frequent_data_update():
    non_frequent_update = non_frequent_banks_update + non_frequent_currency_exchange_update

    for update in non_frequent_update:
        try:
            exchange_data = update()
            time.sleep(2)
            print(update)
            if exchange_data is not None:
                update_company_exchange_data(exchange_data)
        except Exception as err:
            print('Error while updating non frequent data ', err)

    logger.info('Scraped non frequent data update ' + datetime.today().strftime('%Y-%m-%d %H:%M:%S'))


def init_frequent_data_update():
    frequent_updates = frequent_banks_update + frequent_currency_exchange_update

    for update in frequent_updates:
        try:
            exchange_data = update()
            time.sleep(2)
            if exchange_data is not None:
                update_company_exchange_data(exchange_data)
        except Exception as err:
            print('Error while updating frequent data ', err)
    logger.info('Scraped frequent data update ' + datetime.today().strftime('%Y-%m-%d %H:%M:%S'))


init_logger()
# schedule.every(5).hour.do(init_non_frequent_data_update())
schedule.every(2).hours.do(init_non_frequent_data_update)
# schedule.every(3).hour.do(init_frequent_data_update())
schedule.every(1).hours.do(init_frequent_data_update)

while 1:
    # print('IIIII')
    # logger.info('Scraped non frequent data update '+datetime.today().strftime)
    schedule.run_pending()
    time.sleep(1)
