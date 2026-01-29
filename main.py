import time
from datetime import datetime

from src.db.db_handler import DatabaseHandler
from src.util.common_classes.exchange_company import ExchangeCompany
from src.website_scrapers.banks.index import frequent_banks_update, non_frequent_banks_update
from src.website_scrapers.cb.uae_central_bank import scrape_central_bank
from src.website_scrapers.exchange_business.index import frequent_currency_exchange_update, \
    non_frequent_currency_exchange_update, very_rearly_exchange_update

dbHandler = DatabaseHandler()




def update_company_exchange_data(company_exchange_data: ExchangeCompany):
    company = dbHandler.find_company_by_url(company_exchange_data.url)
    if company == None:
        dbHandler.insert_data(company_exchange_data)
    else:
        dbHandler.update_exchange_rate(company_exchange_data)
        # update

def init_very_rare_data_update():
    very_rear_updates = very_rearly_exchange_update

    for update in very_rear_updates:
        try:
            exchange_data = update()
            time.sleep(2)
            print(update)
            if exchange_data is not None:
                update_company_exchange_data(exchange_data)
        except Exception as err:
            print('Error while updating very rear data ', err)

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

def init_central_bank_update():
    scrape_central_bank()

init_central_bank_update()
init_very_rare_data_update()
init_non_frequent_data_update()
init_frequent_data_update()
