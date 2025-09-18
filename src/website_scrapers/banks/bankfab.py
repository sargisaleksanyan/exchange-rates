# First Abu Dhabi Bank
from src.util.common_classes.company import BankExchangeRateUrl
from src.util.scraping_util.request_util import make_get_request_with_proxy


def scrape_first_abu_dhabi():
    content1 = make_get_request_with_proxy('https://api.ipify.org?format=json')
    content = make_get_request_with_proxy(BankExchangeRateUrl.FIRST_ABU_DHABI_BANK)
    m = 5


scrape_first_abu_dhabi()
