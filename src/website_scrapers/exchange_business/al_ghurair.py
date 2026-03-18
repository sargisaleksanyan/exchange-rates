from typing import List
from src.util.common_classes.company_data import ExchangeBusinessNames, ExchangeBusinessExchangeUrl, \
    ExchangeBusinessApiUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, ExchangeRate, Currency, \
    CompanyExchangeRates, ExchangeType
from src.util.scraping_util.request_util import make_get_request_with_proxy
from src.util.tool.json_util import parse_string_to_json, get_value_from_json
from src.util.tool.string_util import convert_to_float, is_float_ok, convert_to_reverse_float

headers = {
    'client-id': 'agex@rate01',
    'client-secret': 'agex@ratepwProd',
    'RequestKey': '123456700WEB01',
    'origin': 'https://www.alghurairexchange.com',
    'referer': 'https://www.alghurairexchange.com'
}

CURRENCY_HEADER = 'Currency'
FOREX_SALE_HEADER = 'FCSale'
FOREX_BUY_HEADER = 'FCPurchase'
TRANSFER_RATE_HEADER = 'TTSale'


def get_exchange_rates(url):
    # TODO make headers extraction dynamic from html page source .
    # content = make_get_request_with_proxy(ExchangeBusinessApiUrl.AL_GHURAIR_EXCHANGE_CASH_RATES, given_headers=headers)
    content = make_get_request_with_proxy(url, given_headers=headers)

    exchange_rates = []

    if (content is not None):
        cash_exchange_rates_data = parse_string_to_json(content)
        if (cash_exchange_rates_data is not None):
            rates = get_value_from_json(cash_exchange_rates_data, 'rate')

            for rate in rates:
                currency_code = get_value_from_json(rate, CURRENCY_HEADER)
                currency = Currency.get_currency(currency_code)

                if currency is not None:
                    sell = convert_to_float(get_value_from_json(rate, FOREX_SALE_HEADER))
                    buy = convert_to_float(get_value_from_json(rate, FOREX_BUY_HEADER))
                    transfer_rate = get_value_from_json(rate, TRANSFER_RATE_HEADER)

                    if is_float_ok(sell) == True and is_float_ok(buy) == True:
                        exchange_data = ExchangeRate(currency.code, buy_rate=buy, sell_rate=sell)
                        exchange_rates.append(exchange_data)
                        
                    elif transfer_rate is not None:
                        transfer_rate_value = convert_to_reverse_float(transfer_rate)
                        if is_float_ok(transfer_rate_value):
                           exchange_data = ExchangeRate(currency.code, rate=transfer_rate_value)
                           exchange_data.set_original_rate(convert_to_float(transfer_rate))
                           exchange_rates.append(exchange_data)
    return exchange_rates


def get_rates_from_al_ghurair() -> List[CompanyExchangeRates] | None:
    # From API I can see that it is getting response but in website I do not see anything

    transfer_rates = get_exchange_rates(ExchangeBusinessApiUrl.AL_GHURAIR_EXCHANGE_TRANSFER_RATES)

    transfer_exchange_rate = CompanyExchangeRates(transfer_rates)
    transfer_exchange_rate.set_exchange_type(ExchangeType.TRANSFER)
    transfer_exchange_rate.set_current_scrape_date()

    return [transfer_exchange_rate]


def scrape_al_ghurair() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_al_ghurair()
        exchange_company = ExchangeCompany(ExchangeBusinessNames.AL_GHURAIR_EXCHANGE,
                                           ExchangeBusinessExchangeUrl.AL_GHURAIR_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)

        exchange_company.set_exchange_rates(company_exchange_rates)

        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping ', ExchangeBusinessNames.AL_GHURAIR_EXCHANGE, err)
    return None
