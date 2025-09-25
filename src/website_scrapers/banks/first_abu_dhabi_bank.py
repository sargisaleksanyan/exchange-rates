# First Abu Dhabi Bank
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup

from src.util.common_classes.company_data import BankExchangeRateUrl, BankName, BankUrl
from src.util.common_classes.exchange_company import ExchangeRate, Currency, CompanyExchangeRates, ExchangeCompany, \
    ExchangeCompanyType
from src.util.tool.json_util import parse_string_to_json
from src.util.scraping_util.request_util import make_get_request_with_proxy
from src.util.tool.string_util import convert_to_float

SITECORE = 'sitecore'
ROUTE = 'route'
CODE = 'Code'
PLACEHOLDERS = 'placeholders'
JSS_MAIN = 'jss-main'
FIELDS = 'fields'
VALUE = 'value'
BUYING = 'Buying'
SELLING = 'Selling'
CURRENCY_PATH = 'CurrencyPath'
UPDATED_DATE_TIME = 'UpdatedDateTime'


def find_json_from_html(html_content: str):
    soup = BeautifulSoup(html_content, 'html.parser')
    json_scripts = soup.find_all('script', type='application/json')

    for json_script in json_scripts:
        json_data = parse_string_to_json(json_script.string.strip())
        if json_data is not None and SITECORE in json_data and ROUTE in json_data[SITECORE]:
            return json_data

    return None


def find_value_by_key_from_fields(json, key: str):
    placeholders = json[SITECORE][ROUTE][PLACEHOLDERS]

    if placeholders != None:
        jss_main_elements = placeholders[JSS_MAIN]

        for jss_main_element in jss_main_elements:
            if (FIELDS in jss_main_element):
                fields = jss_main_element[FIELDS]

                if (fields != None and key in fields):
                    currencies = fields[key]
                    return currencies

    return None


def extract_value_from_fields(json, key):
    if json is not None and key in json:
        object = json[key]
        if VALUE in object:
            return object[VALUE]

    return None


def parse_currency_data(currency_json_data) -> List[ExchangeRate]:
    exchangerates = []

    for currency_data in currency_json_data:
        if (FIELDS in currency_data):
            fields = currency_data[FIELDS]
            currency_code = extract_value_from_fields(fields, CODE)
            if (currency_code != None):
                currency = Currency.get_currency(currency_code)
                if (currency != None):
                    selling = extract_value_from_fields(fields, SELLING)
                    buying = extract_value_from_fields(fields, BUYING)

                    if (selling != None and buying != None):
                        exchangerate = ExchangeRate(currency, convert_to_float(buying), convert_to_float(selling))
                        exchangerates.append(exchangerate)

            else:
                print(currency_code)

    return exchangerates
    # TODO write to log file


# TODO

def extract_update_date(update_date: str):
    try:
        return datetime.strptime(update_date.strip(), "%d %B, %Y %I:%M:%S %p")
    except Exception as err:
        print('Error', err, 'date', update_date)


def scrape_company_exchange_rates(json) -> CompanyExchangeRates:
    currency_json_data = find_value_by_key_from_fields(json, CURRENCY_PATH)
    updated_json_data = find_value_by_key_from_fields(json, UPDATED_DATE_TIME)
    updated_date = extract_update_date(updated_json_data.strip())
    currency_data = parse_currency_data(currency_json_data)
    company_exchange_rates = CompanyExchangeRates(currency_data)
    company_exchange_rates.set_update_date(updated_date)
    company_exchange_rates.set_current_scrape_date()
    return company_exchange_rates


def scrape_first_abu_dhabi_bank_data() -> ExchangeCompany:
    try:
        content = make_get_request_with_proxy(BankExchangeRateUrl.FIRST_ABU_DHABI_BANK)
        if (content is not None):
            json = find_json_from_html(content)
            company_exchange_rates = scrape_company_exchange_rates(json)
            exchange_company = ExchangeCompany(BankName.FIRST_ABU_DHABI_BANK, BankUrl.FIRST_ABU_DHABI_BANK,
                                               ExchangeCompanyType.NATIONAL_BANK)
            exchange_company.set_exchange_rates(company_exchange_rates)
            return exchange_company
    except Exception as err:
        print('Error occured while scraping ', BankName.FIRST_ABU_DHABI_BANK, err)

    return None


