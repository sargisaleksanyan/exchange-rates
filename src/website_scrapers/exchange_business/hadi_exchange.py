# exchange-mny-tab-content
from src.util.common_classes.company_data import ExchangeBusinessNames, ExchangeBusinessUrl, ExchangeBusinessExchangeUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, CompanyExchangeRates, \
    Currency, ExchangeRate, ExchangeType
from src.util.scraping_util.request_util import make_get_request_with_parsed_html
from src.util.tool.string_util import convert_to_float


def scrape_hadi_exchange_rates() -> CompanyExchangeRates | None:
    html = make_get_request_with_parsed_html(ExchangeBusinessExchangeUrl.HADI_EXCHANGE)
    if (html is None):
        return None
    #option_elements = html.select('․option_currency')
    option_elements = html.select(".option.option_currency")

    transfer_rates = []

    if option_elements is not None:
        for option_element in option_elements:
            currency_name = option_element.get('data-type')
            currency = Currency.get_currency(currency_name)
            if currency is None:
                continue
            data_rate = option_element.get('data-rate')
            rate = convert_to_float(data_rate)
            if rate is not None:
                transfer_rate = ExchangeRate(currency.code, rate=rate)
                transfer_rates.append(transfer_rate)

    company_exchange_rates = CompanyExchangeRates(transfer_rates)
    company_exchange_rates.set_current_scrape_date()
    company_exchange_rates.set_exchange_type(ExchangeType.TRANSFER)
    return company_exchange_rates


def scrape_hadi_exchange() -> ExchangeCompany | None:
    try:
        company_exchange_rates = scrape_hadi_exchange_rates()

        if company_exchange_rates is None:
            return None

        exchange_company = ExchangeCompany(ExchangeBusinessNames.HADI_EXCHANGE,
                                           ExchangeBusinessUrl.HADI_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)
        exchange_company.add_exchange_rate(company_exchange_rates)
        # exchange_company.set_exchange_rates(company_exchange_rates)
        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping ', ExchangeBusinessNames.HADI_EXCHANGE, err)
    return None