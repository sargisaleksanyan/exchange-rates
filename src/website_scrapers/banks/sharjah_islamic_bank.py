from typing import List

from src.util.common_classes.company_data import BankName, BankUrl, BankExchangeRateApiUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, CompanyExchangeRates, \
    Currency, ExchangeRate
from src.util.tool.json_util import parse_string_to_json, get_value_from_json, get_value_from_json_by_queue
from src.util.scraping_util.request_util import make_get_request_with_proxy
from src.util.tool.string_util import convert_to_float

CURRENCY_CODE = 'currencyCode'
BUY_RATE = 'buyRate'
SELL_RATE = 'sellRate'


def parse_exchange_date_data(exchange_rates_raw_data) -> List[ExchangeRate]:
    exchange_rates = []
    for exchange_rate_data in exchange_rates_raw_data:
        currency_code = get_value_from_json(exchange_rate_data, CURRENCY_CODE)
        if currency_code is not None:
            currency = Currency.get_currency(currency_code)
            if currency is not None:
                buy_rate = get_value_from_json(exchange_rate_data, BUY_RATE)
                sell_rate = get_value_from_json(exchange_rate_data, SELL_RATE)

                if (sell_rate is not None and buy_rate is not None):
                    exchange_rates.append(
                        ExchangeRate(currency.code, convert_to_float(buy_rate), convert_to_float(sell_rate)))

    return exchange_rates


def get_rates_from_sharjah_islamic_bank() -> CompanyExchangeRates | None:
    content = make_get_request_with_proxy(BankExchangeRateApiUrl.SHARJAH_ISLAMIC_BANK)
    if content is not None:
        json = parse_string_to_json(content)
        if (json is not None):
            data_json_text = get_value_from_json(json, 'data')
            if data_json_text is not None:
                data_json = parse_string_to_json(data_json_text)
                exchange_rates_raw_data = get_value_from_json_by_queue(data_json, 'exchangeRate')
                if (exchange_rates_raw_data is not None):
                    exchange_rates = parse_exchange_date_data(exchange_rates_raw_data)
                    company_exchange_rates = CompanyExchangeRates(exchange_rates)
                    company_exchange_rates.set_current_scrape_date()
                    return company_exchange_rates

    return None

#TODO This company uses cloudflare and has good antiscraping system, manual fix
def scrape_sharjah_islamic_bank() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_sharjah_islamic_bank()
        # company_exchange_rates = parse_rates(raw_rates)
        exchange_company = ExchangeCompany(BankName.SHARJAH_ISLAMIC_BANK,
                                           BankUrl.SHARJAH_ISLAMIC_BANK,
                                           ExchangeCompanyType.NATIONAL_BANK)
        exchange_company.add_exchange_rate(company_exchange_rates)
        # exchange_company.set_exchange_rates(company_exchange_rates)
        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping emirates islamic bank data', err)
    return None

