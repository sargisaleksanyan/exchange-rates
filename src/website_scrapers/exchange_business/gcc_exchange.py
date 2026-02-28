import random
import time

from src.util.common_classes.company_data import ExchangeBusinessNames, ExchangeBusinessExchangeUrl, \
    ExchangeBusinessApiUrl, ExchangeBusinessUrl
from src.util.common_classes.exchange_company import ExchangeCompany, CompanyExchangeRates, ExchangeCompanyType, \
    Currency, ExchangeRate, ExchangeType
from src.util.scraping_util.request_util import make_get_request_with_proxy
from src.util.tool.json_util import parse_string_to_json, get_value_from_json
from src.util.tool.string_util import convert_to_float

CURRENCY_CODE_HEADER = 'CurrencyCode'
CURRENCY_TRANSFER_HEADER = 'ExchangeRate'


def sleep_random_time():
    sleep_time = random.randint(1100, 2100) / 1000
    time.sleep(sleep_time)


def extract_exchange_rates(json_data):
    currency = Currency.get_currency(get_value_from_json(json_data, CURRENCY_CODE_HEADER))
    if currency is not None:
        transfer_rate = get_value_from_json(json_data, CURRENCY_TRANSFER_HEADER)
        if transfer_rate is not None:
            rate = convert_to_float(transfer_rate)
            return ExchangeRate(currency.code, rate=rate)

    return None


def get_rates_from_gcc() -> CompanyExchangeRates | None:
    content = make_get_request_with_proxy(ExchangeBusinessApiUrl.GCC_EXCHANGE)
    if content is None:
        return None

    json_data = parse_string_to_json(content)
    contents = get_value_from_json(json_data, 'exchangerate')
    exchange_rates = []

    if (contents is None):
        return

    for data in contents:
        currency_code = get_value_from_json(data, CURRENCY_CODE_HEADER)
        if currency_code is None and Currency.get_currency(currency_code) is None:
            continue

        exchange_rate = extract_exchange_rates(data)
        if exchange_rate is not None:
            exchange_rates.append(exchange_rate)

    company_exchange_rates = CompanyExchangeRates(exchange_rates)
    company_exchange_rates.set_exchange_type(ExchangeType.TRANSFER)
    company_exchange_rates.set_current_scrape_date()
    return company_exchange_rates


def scrape_gcc_exchange() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_gcc()
        exchange_company = ExchangeCompany(ExchangeBusinessNames.GCC_EXCHANGE,
                                           ExchangeBusinessUrl.GCC_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)
        exchange_company.add_exchange_rate(company_exchange_rates)
        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping ', ExchangeBusinessNames.GCC_EXCHANGE, err)
    return None

