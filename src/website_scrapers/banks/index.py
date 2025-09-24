from src.website_scrapers.banks.abu_dhabi_commercial_bank import scrape_abu_dhabi_commercial_bank
from src.website_scrapers.banks.bankfab import scrape_first_abu_dhabi_bank_data
from src.website_scrapers.banks.emirates_bank import scrape_emiratesnbd_bank_data
from src.website_scrapers.banks.emirates_islamic_bank import scrape_emirates_islamic_bank_data

non_frequent_banks_update = [scrape_abu_dhabi_commercial_bank]

frequent_banks_update = [scrape_first_abu_dhabi_bank_data, scrape_emiratesnbd_bank_data,
                         scrape_emirates_islamic_bank_data]
