from typing import List

from bs4 import BeautifulSoup

from src.util.common_classes.company_data import BankName, BankUrl, BankExchangeRateUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, CompanyExchangeRates, \
    ExchangeRate, Currency
from src.util.scraping_util.browser_util import get_website_content_by_browser
from src.util.tool.json_util import parse_string_to_json, get_value_from_json
from src.util.tool.string_util import convert_to_float

WINDOWS_CURRENCY_DATA = 'window.currencyData ='


# TODO
def parse_json_to_exchange_rates(json_string) -> List[ExchangeRate] | None:
    json_object = parse_string_to_json(json_string)
    if json_object is not None:
        keys = json_object.keys()

        if keys is not None:
            exchange_rates = []
            for key in keys:
                currency_data = json_object[key]
                currency = Currency.get_currency(key)

                if (currency is not None):
                    buy = get_value_from_json(currency_data, 'buy')
                    sell = get_value_from_json(currency_data, 'sell')

                    buy = convert_to_float(buy)
                    sell = convert_to_float(sell)

                    if buy is not None and sell is not None:
                        exchange_data = ExchangeRate(currency.code, buy, sell)
                        exchange_rates.append(exchange_data)

            return exchange_rates


def get_rates_from_national_bank_of_fujairah() -> CompanyExchangeRates | None:
    content = get_website_content_by_browser(BankExchangeRateUrl.NATIONAL_BANK_OF_FUJARAH, wait_time=10)

    if content is not None:
        soup = BeautifulSoup(content, 'html.parser')
        json_scripts = soup.find_all('script')
        for json_script in json_scripts:
            if (json_script is not None and json_script.string is not None):
                json_string = json_script.string

                if 'currencyData' in json_string:
                    json_string = json_string.replace(WINDOWS_CURRENCY_DATA, '')

                    if json_string.endswith(';'):
                        json_string = json_string[0: len(json_string) - 1]

                    exchange_rates = parse_json_to_exchange_rates(json_string)

                    if exchange_rates is not None:
                        company_exchange_rates = CompanyExchangeRates(exchange_rates)
                        company_exchange_rates.set_current_scrape_date()
                        return company_exchange_rates
                    # todo add update date

    return None


# have to scrape very rarely because it might show an error
def scrape_national_bank_of_fujairah() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_national_bank_of_fujairah()
        exchange_company = ExchangeCompany(BankName.NATIONAL_BANK_OF_FUJARAH,
                                           BankUrl.NATIONAL_BANK_OF_FUJARAH,
                                           ExchangeCompanyType.NATIONAL_BANK)
        exchange_company.add_exchange_rate(company_exchange_rates)
        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping emirates islamic bank data', err)
    return None


scrape_national_bank_of_fujairah()