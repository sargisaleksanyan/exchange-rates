from src.website_scrapers.banks.abu_dhabi_commercial_bank import scrape_abu_dhabi_commercial_bank
from src.website_scrapers.banks.ajmanbank import scrape_ajman_bank
from src.website_scrapers.banks.commercial_bank_of_dubai import scrape_commercial_bank_of_dubai
from src.website_scrapers.banks.dubai_islamic_bank import scrape_dubai_islamic_bank
from src.website_scrapers.banks.first_abu_dhabi_bank import scrape_first_abu_dhabi_bank_data
from src.website_scrapers.banks.emirates_bank import scrape_emiratesnbd_bank_data
from src.website_scrapers.banks.emirates_islamic_bank import scrape_emirates_islamic_bank_data
from src.website_scrapers.banks.national_bank_of_ras_al_khaimah import scrape_national_bank_of_ras_al_khaimah
from src.website_scrapers.banks.sharjah_islamic_bank import scrape_sharjah_islamic_bank

non_frequent_banks_update = [scrape_abu_dhabi_commercial_bank, scrape_commercial_bank_of_dubai, scrape_ajman_bank]

frequent_banks_update = [scrape_first_abu_dhabi_bank_data, scrape_emiratesnbd_bank_data,
                         scrape_national_bank_of_ras_al_khaimah,
                         scrape_emirates_islamic_bank_data, scrape_sharjah_islamic_bank, scrape_dubai_islamic_bank]
