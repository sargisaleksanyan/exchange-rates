from src.db.db_handler import DatabaseHandler
from src.util.common_classes.exchange_company import ExchangeCompany
from src.website_scrapers.banks.index import frequent_banks_update, non_frequent_banks_update

dbHandler = DatabaseHandler()


def update_company_exchange_data(company_exchange_data: ExchangeCompany):
    company = dbHandler.find_company_by_url(company_exchange_data.url)
    if company == None:
        dbHandler.insert_data(company_exchange_data)
    else:
        dbHandler.update_exchange_rate(company_exchange_data)
        # update


def init_non_frequent_data_update():
    non_frequent_update = non_frequent_banks_update

    for update in non_frequent_update:
        exchange_data = update()
        if exchange_data is not None:
            update_company_exchange_data(exchange_data)

def init_frequent_data_update():
    frequent_updates = frequent_banks_update

    for update in frequent_updates:
        exchange_data = update()
        if exchange_data is not None:
            update_company_exchange_data(exchange_data)


init_non_frequent_data_update()
init_frequent_data_update()
