from src.util.common_classes.company_data import ExchangeBusinessNames, ExchangeBusinessUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, CompanyExchangeRates, \
    Currency, ExchangeRate, ExchangeType
from src.util.scraping_util.request_util import make_get_request_with_proxy
from src.util.tool.json_util import parse_string_to_json, get_value_from_json_by_queue, get_value_from_json
from src.util.tool.string_util import convert_to_float


#
def scrape_lulu_exchange_rates() -> CompanyExchangeRates | None:
    response = make_get_request_with_proxy(
        'https://lieservices.luluone.com:9443/liveccyrates?payload=%7B%22activityType%22%3A%22rates.get%22%2C%22aglcid%22%3A784278%2C%22instype%22%3A%22LR%22%7D')
    if response is None:
        return None
    json = parse_string_to_json(response)
    rates = get_value_from_json_by_queue(json, 'rates')
    transfer_rates = []

    if rates is not None and len(rates) > 0:
        for rate in rates:
            currency_value = get_value_from_json(rate, 'toccy')
            rate_value = get_value_from_json(rate, 'rate')

            if (currency_value is not None and rate_value is not None):
                currency = Currency.get_currency(currency_value)
                if currency is None:
                    continue
                rate_number = convert_to_float(rate_value)
                if rate_number is None:
                    continue
                transfer_rate = ExchangeRate(currency.code, rate_number)
                transfer_rates.append(transfer_rate)

    company_exchange_rates = CompanyExchangeRates(transfer_rates)
    company_exchange_rates.set_current_scrape_date()

    company_exchange_rates.set_exchange_type(ExchangeType.TRANSFER)
    return company_exchange_rates


# Currently scraped only transfer rates but it also has sell and buy rates
def scrape_lulu_exchange() -> ExchangeCompany | None:
    try:
        company_exchange_rates = scrape_lulu_exchange_rates()

        if company_exchange_rates is None:
            return None

        exchange_company = ExchangeCompany(ExchangeBusinessNames.LULU_EXCHANGE,
                                           ExchangeBusinessUrl.LULU_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)
        exchange_company.add_exchange_rate(company_exchange_rates)
        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping ', ExchangeBusinessNames.LULU_EXCHANGE, err)
    return None
