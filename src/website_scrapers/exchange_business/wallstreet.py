from datetime import datetime
from locale import currency

from src.util.common_classes.company_data import ExchangeBusinessNames, ExchangeBusinessExchangeUrl, \
    ExchangeBusinessApiUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, ExchangeRate, Currency, \
    CompanyExchangeRates
from src.util.scraping_util.request_util import make_get_request_with_proxy
from src.util.tool.json_util import parse_string_to_json, get_value_from_json
from src.util.tool.string_util import convert_to_float


def convert_update_date(update_date: str):
    if update_date != None:
        # date_obj = datetime.strptime(last_update_date, "%m/%d/%Y %I:%M:%S %p")
        # date = datetime.strptime(update_date, "%d %m %Y %I:%M %p")  # TODO check if this correct
        date = datetime.strptime(update_date, "%d %b %Y %H:%M %p")  #
        return date

    return None


def get_rates_from_wall_street() -> CompanyExchangeRates | None:
    json_data_string = make_get_request_with_proxy(ExchangeBusinessApiUrl.WALL_STREET_EXCHANGE)
    if (json_data_string is not None):

        json_data = parse_string_to_json(json_data_string)
        if json_data is not None:

            exchange_rates_data = get_value_from_json(json_data, 'data')
            if exchange_rates_data and len(exchange_rates_data) > 0:
                exchange_rates = []

                for exchange_rate_data in exchange_rates_data:
                    currency_code = get_value_from_json(exchange_rate_data, 'currencyCode')
                    if currency_code is None:
                        continue

                    currency = Currency.get_currency(currency_code)

                    if currency is not None:
                        buy = get_value_from_json(exchange_rate_data, 'buyRate')
                        sell = get_value_from_json(exchange_rate_data, 'sellRate')
                        exchange_rate = ExchangeRate(currency.code, convert_to_float(buy), convert_to_float(sell))
                        exchange_rates.append(exchange_rate)

                company_exchange_rate = CompanyExchangeRates(exchange_rates)
                company_exchange_rate.set_current_scrape_date()
                update_date = convert_update_date(get_value_from_json(json_data, 'date'))

                if update_date is not None:
                    company_exchange_rate.set_update_date(update_date)
                return company_exchange_rate
    return None


def scrape_wall_street() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_wall_street()
        exchange_company = ExchangeCompany(ExchangeBusinessNames.WALL_STREET_EXCHANGE,
                                           ExchangeBusinessExchangeUrl.WALL_STREET_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)

        exchange_company.add_exchange_rate(company_exchange_rates)

        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping emirates islamic bank data', err)
    return None
