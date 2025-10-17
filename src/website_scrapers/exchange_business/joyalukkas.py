import random
import time

from src.util.common_classes.company_data import ExchangeBusinessNames, ExchangeBusinessExchangeUrl, \
    ExchangeBusinessApiUrl
from src.util.common_classes.exchange_company import ExchangeCompany, CompanyExchangeRates, ExchangeCompanyType, \
    Currency, ExchangeRate
from src.util.scraping_util.request_util import make_get_request_with_proxy
from src.util.tool.json_util import parse_string_to_json, get_value_from_json
from src.util.tool.string_util import convert_to_float

CURRENCY_CODE_HEADER = 'CURRENCY_CODE'
CURRENCY_BUY_HEADER = 'FXBUYRATE'
CURRENCY_SELL_HEADER = 'FXSELLRATE'


# AFA ARS
def get_sell_rate(currency_code):
    sell_rate_url = "https://admin.joyalukkasexchange.com/api/currency-converter?region=2&amount=1&currency_code=" + currency_code + "&rate_type=FXS&amount_type=FCY"
    content = make_get_request_with_proxy(sell_rate_url)
    if content is None:
        return None
    json_data = parse_string_to_json(content)
    exchange_data_list = get_value_from_json(json_data, 'data')
    if exchange_data_list is not None:
        for exchange_data in exchange_data_list:
            data_currency_code = get_value_from_json(exchange_data, CURRENCY_CODE_HEADER)
            if data_currency_code == currency_code:
                return get_value_from_json(exchange_data, 'RATE')
    return None


def sleep_random_time():
    sleep_time = random.randint(1100, 2100) / 1000
    time.sleep(sleep_time)


def extract_exchange_rates(json_data):
    currency_code = get_value_from_json(json_data, CURRENCY_CODE_HEADER)
    sell_rate = get_value_from_json(json_data, CURRENCY_SELL_HEADER)
    buy_rate = get_value_from_json(json_data, CURRENCY_BUY_HEADER)
    currency = Currency.get_currency(currency_code)
    if currency is not None:
        sell = convert_to_float(sell_rate)
        buy = convert_to_float(buy_rate)
        if sell > 0 and buy > 0 and sell >= buy:
            return ExchangeRate(currency.code, buy_rate=buy, sell_rate=sell)

    return None


def get_rates_from_joyalukkas() -> CompanyExchangeRates | None:
    content = make_get_request_with_proxy(ExchangeBusinessApiUrl.JOYALUKKAS_EXCHANGE)
    if content is None:
        return None

    json_data = parse_string_to_json(content)
    contents = get_value_from_json(json_data, 'contents')
    exchange_rates = []

    for data in contents:
        currency_code = get_value_from_json(data, CURRENCY_CODE_HEADER)
        if currency_code is None or currency_code == 'AED' and Currency.get_currency(currency_code) is None:
            continue

        buy_rate = convert_to_float(get_value_from_json(data, CURRENCY_BUY_HEADER))
        sell_rate = convert_to_float(get_value_from_json(data, CURRENCY_SELL_HEADER))

        if buy_rate > 0 and sell_rate > 0:
            if (sell_rate == buy_rate):
                sleep_random_time()
                individual_sell_rate = get_sell_rate(currency_code)
                if individual_sell_rate is None:
                    continue
                data[CURRENCY_SELL_HEADER] = individual_sell_rate
            exchange_rate = extract_exchange_rates(data)
            if exchange_rate is not None:
                exchange_rates.append(exchange_rate)

    print('Length ', len(exchange_rates))
    company_exchange_rates = CompanyExchangeRates(exchange_rates)
    company_exchange_rates.set_current_scrape_date()
    return company_exchange_rates


def scrape_joyalukkas_exchange() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_joyalukkas()
        # company_exchange_rates = parse_rates(raw_rates)
        exchange_company = ExchangeCompany(ExchangeBusinessNames.JOYALUKKAS_EXCHANGE,
                                           ExchangeBusinessExchangeUrl.JOYALUKKAS_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)
        exchange_company.add_exchange_rate(company_exchange_rates)
        # exchange_company.set_exchange_rates(company_exchange_rates)
        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping ', ExchangeBusinessNames.JOYALUKKAS_EXCHANGE, err)
    return None

# Currency has not been found AFA
# Currency has not been found BWP
# Currency has not been found CSD
# Currency has not been found GHC
# Currency has not been found HRK
# Currency has not been found MOP
# Currency has not been found SCP
# Currency has not been found SCR
# Currency has not been found SDP
# Currency has not been found SUS
# Currency has not been found TRL
# Currency has not been found TUM
# Currency has not been found YER
