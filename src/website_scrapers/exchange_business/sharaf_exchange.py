from datetime import datetime, timedelta
from typing import List

from src.util.common_classes.company_data import ExchangeBusinessNames, ExchangeBusinessExchangeUrl, \
    ExchangeBusinessApiUrl, ExchangeBusinessUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, ExchangeRate, Currency, \
    CompanyExchangeRates, ExchangeType
from src.util.scraping_util.request_util import make_get_request_with_proxy
from src.util.tool.json_util import parse_string_to_json, get_value_from_json
from src.util.tool.string_util import convert_to_float, convert_to_reverse_float


def convert_update_date(update_date: str):
    if update_date != None:
        # date_obj = datetime.strptime(last_update_date, "%m/%d/%Y %I:%M:%S %p")
        # date = datetime.strptime(update_date, "%d %m %Y %I:%M %p")  # TODO check if this correct
        date = datetime.strptime(update_date, "%Y-%m-%d %I:%M %p")  #
        return date

    return None


def is_update_date_fresh(update_date):
    two_days_ago = datetime.now() - timedelta(days=2)
    return update_date > two_days_ago


def get_rates_from_sharaf_exchange() -> List[CompanyExchangeRates] | None:
    json_data_string = make_get_request_with_proxy(ExchangeBusinessApiUrl.SHARAF_EXCHANGE)
    if (json_data_string is not None):

        json_data = parse_string_to_json(json_data_string)
        if json_data is not None:

            data = get_value_from_json(json_data, 'data')
            if (data is None):
                return

            exchange_rates_data = get_value_from_json(data, 'details')
            if (exchange_rates_data is None):
                return

            if exchange_rates_data and len(exchange_rates_data) > 0:
                cash_exchange_rates = []
                transfer_exchange_rates = []

                for exchange_rate_data in exchange_rates_data:
                    currency_code = get_value_from_json(exchange_rate_data, 'currency_code')
                    if currency_code is None:
                        continue

                    currency = Currency.get_currency(currency_code)

                    if currency is not None:
                        last_update = get_value_from_json(exchange_rate_data, 'last_update')
                        if (last_update is None):
                            continue
                        last_update = convert_update_date(last_update)
                        if (is_update_date_fresh(last_update) == False):
                            continue

                        buy = get_value_from_json(exchange_rate_data, 'fc_buy')
                        sell = get_value_from_json(exchange_rate_data, 'fc_sell')
                        transfer_rate = get_value_from_json(exchange_rate_data, 'dd_tt')

                        if (buy is not None and sell is not None):
                            exchange_rate = ExchangeRate(currency.code, convert_to_reverse_float(buy),
                                                         convert_to_reverse_float(sell))
                            exchange_rate.set_original_sell_rate(convert_to_float(sell))
                            exchange_rate.set_original_buy_rate(convert_to_float(buy))
                            cash_exchange_rates.append(exchange_rate)

                        if (transfer_rate is not None):
                            exchange_rate = ExchangeRate(currency.code, rate=convert_to_reverse_float(transfer_rate))
                            exchange_rate.set_original_rate(convert_to_float(transfer_rate))
                            transfer_exchange_rates.append(exchange_rate)

                company_cash_exchange_rate = CompanyExchangeRates(cash_exchange_rates)
                company_cash_exchange_rate.set_exchange_type(ExchangeType.CASH)
                company_cash_exchange_rate.set_current_scrape_date()

                company_transfer_exchange_rate = CompanyExchangeRates(transfer_exchange_rates)
                company_transfer_exchange_rate.set_exchange_type(ExchangeType.TRANSFER)
                company_transfer_exchange_rate.set_current_scrape_date()

                return [company_cash_exchange_rate, company_transfer_exchange_rate]

            # update_date = convert_update_date(get_value_from_json(json_data, 'date'))

    return None


def scrape_sharaf_exchange() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_sharaf_exchange()
        exchange_company = ExchangeCompany(ExchangeBusinessNames.SHARAF_EXCHANGE,
                                           ExchangeBusinessUrl.SHARAF_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)

        exchange_company.add_exchange_rate(company_exchange_rates)

        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping emirates islamic bank data', err)
    return None
