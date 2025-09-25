from datetime import datetime

from bs4 import BeautifulSoup

from src.util.common_classes.company_data import BankName, BankUrl, BankExchangeRateUrl, BankExchangeRateApiUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, ExchangeRate, Currency, \
    CompanyExchangeRates
from src.util.tool.json_util import parse_string_to_json, get_value_from_json, get_value_from_json_by_array
from src.util.scraping_util.request_util import make_get_request_with_proxy, make_post_request_with_proxy
from src.util.tool.string_util import convert_to_float

EXCLUDED_CURRENCIES_KEY = 'excludedCurrencies'
FIXED_CURRENCY_CODE = 'fixedCurrencyCode'
FILE_DATE_KEY = 'fileDate'
SELL_RATE_KEY = 'sellRate'
BUY_RATE_KEY = 'buyRate'
FOREX_RATES_KEY = 'forexRates'


def parse_update_date(date_string):
    if (date_string is not None):
        return datetime.strptime(date_string, "%m/%d/%Y %I:%M:%S %p")
    return None


# In system in the first page there are excluded rates which provides while querying rates to exlcude rates

def get_excluded_rates_from_json():
    content = make_get_request_with_proxy(BankExchangeRateUrl.NATIONAL_BANK_OF_RAS_AL_KHAIMAH)
    if (content is not None):
        soup = BeautifulSoup(content, 'html.parser')
        json_script = soup.find('script', id='__NEXT_DATA__')

        if json_script is not None:
            json_data = parse_string_to_json(json_script.string.strip())
            fallback = get_value_from_json_by_array(json_data, ['props', 'pageProps', 'fallback'])
            if (fallback != None):
                keys = fallback.keys()
                if keys is not None:
                    for key in keys:
                        excluded_rates = get_value_from_json(fallback[key], EXCLUDED_CURRENCIES_KEY)
                        if excluded_rates is not None:
                            return excluded_rates
    return None


def get_rates_from_national_bank_of_ras_al_khaimah() -> CompanyExchangeRates | None:
    excluded_currencies = get_excluded_rates_from_json()
    body = {}

    if excluded_currencies is not None:
        # body[EXCLUDED_CURRENCIES_KEY] = "\"" + excluded_currencies + "\""
        # body[EXCLUDED_CURRENCIES_KEY] = "\"" + excluded_currencies + "\""
        body = {
            'excludedCurrencies': excluded_currencies
        }

    content = make_post_request_with_proxy(BankExchangeRateApiUrl.NATIONAL_BANK_OF_RAS_AL_KHAIMAH, body=body,
                                           is_url_encoded=False)
    if content is not None:
        forex_json = parse_string_to_json(content)
        if forex_json is not None and 'responseContent' in forex_json:
            currency_response_string = forex_json['responseContent']
            currency_rates_data = parse_string_to_json(currency_response_string)

            if (currency_rates_data != None and FOREX_RATES_KEY in currency_rates_data):
                exchange_rates = []
                currency_rates = get_value_from_json(currency_rates_data, FOREX_RATES_KEY)
                if (currency_rates is not None):
                    for currency_rate in currency_rates:
                        currency_code = currency_rate[FIXED_CURRENCY_CODE]
                        currency = Currency.get_currency(currency_code)
                        if (currency is not None):
                            buying = get_value_from_json(currency_rate, BUY_RATE_KEY)
                            selling = get_value_from_json(currency_rate, SELL_RATE_KEY)
                            exchange_rate = ExchangeRate(currency, convert_to_float(buying), convert_to_float(
                                selling))  # TODO it is not nessasry to have buying rate or sellin rate
                            exchange_rates.append(exchange_rate)

                    company_exchange_rates = CompanyExchangeRates(exchange_rates)
                    file_date = get_value_from_json(currency_rates_data, FILE_DATE_KEY)
                    update_date = parse_update_date(file_date)

                    if update_date != None:
                        company_exchange_rates.set_update_date(update_date)
                    company_exchange_rates.set_current_scrape_date()
                    return company_exchange_rates

        return None


# if SITECORE in json_data and ROUTE in json_data[SITECORE]:


def scrape_national_bank_of_ras_al_khaimah() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_national_bank_of_ras_al_khaimah()
        # company_exchange_rates = parse_rates(raw_rates)
        exchange_company = ExchangeCompany(BankName.NATIONAL_BANK_OF_RAS_AL_KHAIMAH,
                                           BankUrl.NATIONAL_BANK_OF_RAS_AL_KHAIMAH,
                                           ExchangeCompanyType.NATIONAL_BANK)
        exchange_company.set_exchange_rates(company_exchange_rates)
        # exchange_company.set_exchange_rates(company_exchange_rates)
        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping emirates islamic bank data', err)
    return None
