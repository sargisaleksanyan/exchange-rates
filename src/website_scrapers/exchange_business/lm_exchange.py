from typing import List
from src.util.common_classes.company_data import ExchangeBusinessNames, ExchangeBusinessExchangeUrl, \
    ExchangeBusinessApiUrl, ExchangeBusinessUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, ExchangeRate, Currency, \
    CompanyExchangeRates, ExchangeType
from src.util.scraping_util.request_util import make_get_request_with_proxy
from src.util.tool.json_util import parse_string_to_json, get_value_from_json
from src.util.tool.string_util import convert_to_float, is_float_ok, convert_to_reverse_float

headers = {

    'origin': 'https://lm-exchange.com',
    'referer': 'https://lm-exchange.com'
}

CURRENCY_HEADER = 'currencyCode'
FOREX_SELL_HEADER = 'sellRate'
FOREX_BUY_HEADER = 'buyRate'
TRANSFER_RATE_HEADER = 'ttRate'


def get_exchange_rates(url):
    # TODO make headers extraction dynamic from html page source .
    # content = make_get_request_with_proxy(ExchangeBusinessApiUrl.AL_GHURAIR_EXCHANGE_CASH_RATES, given_headers=headers)
    content = make_get_request_with_proxy(url, given_headers=headers)

    exchange_rates = []

    if (content is not None):
        rates = parse_string_to_json(content)
        if (rates is not None):

            for rate in rates:
                currency_code = get_value_from_json(rate, CURRENCY_HEADER)
                currency = Currency.get_currency(currency_code)

                if currency is not None:
                    # Not taking buy and sell rate because they are being updated very rearly
                    #    sell = convert_to_float(get_value_from_json(rate, FOREX_SALE_HEADER))
                    #  buy = convert_to_float(get_value_from_json(rate, FOREX_BUY_HEADER))
                    transfer_rate = get_value_from_json(rate, TRANSFER_RATE_HEADER)

                    #  if is_float_ok(sell) == True and is_float_ok(buy) == True:
                    #      exchange_data = ExchangeRate(currency.code, buy_rate=buy, sell_rate=sell)
                    #      exchange_rates.append(exchange_data)

                    if transfer_rate is not None:
                        transfer_rate_value = convert_to_reverse_float(transfer_rate)
                        if is_float_ok(transfer_rate_value):
                            exchange_data = ExchangeRate(currency.code, rate=transfer_rate_value)
                            exchange_data.set_original_rate(convert_to_float(transfer_rate))
                            exchange_rates.append(exchange_data)
    return exchange_rates


def get_rates_from_lm_exchange() -> List[CompanyExchangeRates] | None:
    # From API I can see that it is getting response but in website I do not see anything

    transfer_rates = get_exchange_rates(ExchangeBusinessApiUrl.LM_EXCHANGE)

    transfer_exchange_rate = CompanyExchangeRates(transfer_rates)
    transfer_exchange_rate.set_exchange_type(ExchangeType.TRANSFER)
    transfer_exchange_rate.set_current_scrape_date()

    return [transfer_exchange_rate]


def scrape_lm_exchange() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_lm_exchange()
        exchange_company = ExchangeCompany(ExchangeBusinessNames.LM_EXCHANGE,
                                           ExchangeBusinessUrl.LM_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)

        exchange_company.set_exchange_rates(company_exchange_rates)

        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping ', ExchangeBusinessNames.AL_GHURAIR_EXCHANGE, err)
    return None

