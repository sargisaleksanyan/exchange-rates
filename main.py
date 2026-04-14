import time

from src.db.db_handler import DatabaseHandler
from src.util.common_classes.exchange_company import ExchangeCompany
from src.website_scrapers.banks.index import frequent_banks_update, non_frequent_banks_update, very_rear_banks_update
from src.website_scrapers.cb.uae_central_bank import scrape_central_bank
from src.website_scrapers.exchange_business.index import frequent_currency_exchange_update, \
    non_frequent_currency_exchange_update, very_rear_exchange_update

dbHandler = DatabaseHandler()


def is_company_exchange_rates_data_ok(company_exchange_data: ExchangeCompany):
    company_exchange_rates =  company_exchange_data.company_exchange_rates
    is_ok = False
    if company_exchange_rates is None or len(company_exchange_rates) == 0:
        return False
    for company_exchange_rate in company_exchange_rates:
        if company_exchange_rate is not None and company_exchange_rate.exchange_rates is not None and len(company_exchange_rate.exchange_rates)>0:
            return True
    return is_ok


def update_company_exchange_data(company_exchange_data: ExchangeCompany):
    if is_company_exchange_rates_data_ok(company_exchange_data) == True:
       company = dbHandler.find_company_by_url(company_exchange_data.url)
       if company == None:
           dbHandler.insert_data(company_exchange_data)
       else:
           dbHandler.update_exchange_rate(company_exchange_data)
        # update

def init_very_rare_data_update():
    very_rear_updates = very_rear_exchange_update + very_rear_banks_update

    for update in very_rear_updates:
        try:
            exchange_data = update()
            time.sleep(2)
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
    try:
       central_bank_data =  scrape_central_bank()
       update_company_exchange_data(central_bank_data)
    except Exception as err:
        print('Error while updating central bank data ', err)

init_frequent_data_update()
init_central_bank_update()
init_very_rare_data_update()
init_non_frequent_data_update()
