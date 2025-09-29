from datetime import datetime

from bs4 import BeautifulSoup

from src.util.common_classes.company_data import BankExchangeRateUrl, BankExchangeRateApiUrl, BankName, BankUrl
from src.util.common_classes.exchange_company import ExchangeRate, Currency, ExchangeCompany, CompanyExchangeRates, \
    ExchangeCompanyType
from src.util.tool.json_util import parse_string_to_json
from src.util.scraping_util.request_util import make_get_request_with_proxy, make_post_request_with_proxy
from src.util.tool.string_util import convert_to_float

# https://www.emiratesnbd.com/en/foreign-exchange

DATA_SETTINGSID = 'data-settingsid'


def get_data_settingsid() -> str | None:
    content = make_get_request_with_proxy(BankExchangeRateUrl.EMIRATES_ISLAMIC_BANK)
    if (content != None):
        soup = BeautifulSoup(content, 'html.parser')
        convertcurrency_element = soup.select_one("#currency-rate")
        # transfercurrency_element = soup.select_one("#transfercurrency") transferCountries,convertcurrency ,transfercurrency TODO add this
        if convertcurrency_element is not None:
            attr = convertcurrency_element.get(DATA_SETTINGSID)
            return attr
    return None


def get_rates_from_emirates_islamic_bank():
    data_settings_id = get_data_settingsid()
    if data_settings_id is not None:
        body = {
            'SettingsId': data_settings_id,
            'Language': 'en',
            'DecimalPlaces': '6'
        }

        content = make_post_request_with_proxy(BankExchangeRateApiUrl.EMIRATES_ISLAMIC_BANK, body, is_url_encoded=True)
        if (content is not None):
            json_data = parse_string_to_json(content.strip())
            return json_data

    return None


# transfercurrency_element = soup.select_one("#transfercurrency")
def get_data_from_json(data, key):
    if key in data:
        return data[key]

    return None


def get_last_update_date(last_update_date: str):
    if last_update_date != None:
        # date_obj = datetime.strptime(last_update_date, "%m/%d/%Y %I:%M:%S %p")
        date = datetime.strptime(last_update_date, "%d/%m/%Y %I:%M:%S %p")  # TODO check if this correct
        return date

    return None


def parse_rates(rates_raw_data) -> CompanyExchangeRates:
    exchange_rates = []
    rates_data = get_data_from_json(rates_raw_data, 'Currencies')
    last_update_date = get_last_update_date(get_data_from_json(rates_raw_data, 'LastUpdated'))

    for rate_data in rates_data:
        currency_code = get_data_from_json(rate_data, 'CurrencyCode')
        if (currency_code != None):
            currency = Currency.get_currency(currency_code)
            buying = get_data_from_json(rate_data, 'CustomerBuy')
            selling = get_data_from_json(rate_data, 'CustomerSell')
            if (buying != None and selling != None):
                exchangerate = ExchangeRate(currency.code, convert_to_float(buying), convert_to_float(selling))
                exchange_rates.append(exchangerate)

    company_exchange_rates = CompanyExchangeRates(exchange_rates)

    if last_update_date is not None:
        company_exchange_rates.set_update_date(last_update_date)

    company_exchange_rates.set_current_scrape_date()
    return company_exchange_rates


def scrape_emirates_islamic_bank_data() -> ExchangeCompany | None:
    try:
        raw_rates = get_rates_from_emirates_islamic_bank()
        company_exchange_rates = parse_rates(raw_rates)
        exchange_company = ExchangeCompany(BankName.EMIRATES_ISLAMIC_BANK, BankUrl.EMIRATES_ISLAMIC_BANK,
                                           ExchangeCompanyType.NATIONAL_BANK)
        exchange_company.add_exchange_rate(company_exchange_rates)
        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping emirates islamic bank data', err)
    return None
