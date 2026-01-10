from datetime import datetime
from typing import List

from src.util.common_classes.company_data import ExchangeBusinessNames, ExchangeBusinessExchangeUrl, \
    ExchangeBusinessApiUrl, ExchangeBusinessUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, Currency, ExchangeRate, \
    CompanyExchangeRates, ExchangeType
from src.util.scraping_util.request_util import make_get_request_with_proxy
from src.util.tool.json_util import get_value_from_json, parse_string_to_json
from src.util.tool.string_util import convert_to_reverse_float


def get_rate_from_string(rate_data):
    if 'Rate' in rate_data:
        rate = rate_data['Rate']
        if rate.startswith('.'):
            rate = '0' + rate
        return convert_to_reverse_float(rate)
    return None


def get_update_date(rate_data):
    try:
        if 'LastUpdatedOnDateFormattedString' in rate_data:
            last_updated_date = rate_data['LastUpdatedOnDateFormattedString']
            dt = datetime.strptime(last_updated_date, "%d %b %Y %I.%M %p")
            return dt
    except Exception as err:
        print('Error while getting update date ', ExchangeBusinessNames.ORIENT_EXCHANGE, err)
    return None


def get_currency_data(url: str):
    currency_raw_data_string = make_get_request_with_proxy(url)
    if currency_raw_data_string is not None:
        currency_raw_data = parse_string_to_json(currency_raw_data_string)
        rate_list = get_value_from_json(currency_raw_data, 'rateList')

        if currency_raw_data is None or rate_list is None:
            return None

        currency_data = {}

        for rate_data in rate_list:
            currency_code = rate_data['CurrencyCode']
            if currency_code is not None:
                currency_data[currency_code] = rate_data

        return currency_data


def get_rates_from_orient_exchange() -> List[CompanyExchangeRates]:
    cash_buy_rates = get_currency_data(ExchangeBusinessApiUrl.ORIENT_EXCHANGE_BUY_RATES)
    cash_sell_rates = get_currency_data(ExchangeBusinessApiUrl.ORIENT_EXCHANGE_SELL_RATES)

    keys = list(cash_buy_rates.keys() | cash_sell_rates.keys())

    cash_exchange_rates = []
    transfer_rates = []

    for key in keys:
        currency = Currency.get_currency(key)
        if currency is not None:
            cash_buy_data = get_value_from_json(cash_buy_rates, key)
            cash_sell_data = get_value_from_json(cash_sell_rates, key)

            if (cash_sell_data is not None and cash_buy_data is not None):
                exchange_rate = ExchangeRate(currency.code, get_rate_from_string(cash_buy_data),
                                             get_rate_from_string(cash_sell_data))
                exchange_rate.set_update_date(get_update_date(cash_buy_data))
                cash_exchange_rates.append(exchange_rate)

    # tranfer_rates = get_currency_data(ExchangeBusinessApiUrl.ORIENT_EXCHANGE_TRANSFER)
    transfer_rates_content = make_get_request_with_proxy(ExchangeBusinessApiUrl.ORIENT_EXCHANGE_TRANSFER)
    transfer_rates_raw_data_json = parse_string_to_json(transfer_rates_content)
    transfer_rates_raw_data = get_value_from_json(transfer_rates_raw_data_json, 'rateList')
    for transfer_rate_raw_data in transfer_rates_raw_data:
        currency_code = get_value_from_json(transfer_rate_raw_data, 'CurrencyCode')
        if currency_code is not None and Currency.get_currency(currency_code) is not None:
            currency = Currency.get_currency(currency_code)
            exchange_rate = ExchangeRate(currency.code, rate=get_rate_from_string(transfer_rate_raw_data))
            exchange_rate.set_update_date(get_update_date(transfer_rate_raw_data))
            transfer_rates.append(exchange_rate)

    cash_exchange_rates = CompanyExchangeRates(cash_exchange_rates)
    cash_exchange_rates.set_exchange_type(ExchangeType.CASH)
    cash_exchange_rates.set_current_scrape_date()

    transfer_exchange_rates = CompanyExchangeRates(transfer_rates)
    transfer_exchange_rates.set_exchange_type(ExchangeType.TRANSFER)
    transfer_exchange_rates.set_current_scrape_date()

    return [cash_exchange_rates, transfer_exchange_rates]


# Because need to make 3 requests it would be better not to scrape frequently
def scrape_orient_exchange() -> ExchangeCompany | None:
    try:
        exchange_company = ExchangeCompany(ExchangeBusinessNames.ORIENT_EXCHANGE,
                                           ExchangeBusinessUrl.ORIENT_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)

        company_exchange_rates = get_rates_from_orient_exchange()

        exchange_company.set_exchange_rates(company_exchange_rates)

        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping orient exchange business ', ExchangeBusinessNames.ORIENT_EXCHANGE, err)
    # return None

# scrape_orient_exchange()
