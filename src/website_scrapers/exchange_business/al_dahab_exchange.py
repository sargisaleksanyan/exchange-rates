# exchange-mny-tab-content
from src.util.common_classes.company_data import ExchangeBusinessNames, ExchangeBusinessUrl, ExchangeBusinessExchangeUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, CompanyExchangeRates, \
    Currency, ExchangeRate, ExchangeType
from src.util.scraping_util.request_util import make_get_request_with_parsed_html
from src.util.tool.string_util import convert_to_float


def scrape_al_dahab_exchange_rates() -> CompanyExchangeRates | None:
    html = make_get_request_with_parsed_html(ExchangeBusinessExchangeUrl.AL_DAHAB_EXCHANGE)
    if (html is None):
        return None
    # option_elements = html.select('․option_currency')
    list_elements = html.select(".currecymarquee > ul > li")

    transfer_rates = []

    if list_elements is not None:
        for list_element in list_elements:
            text = list_element.getText()
            if text is None:
                continue
            values = text.split('=')
            if len(values) > 1:
                currency_name = values[0].strip().replace('AED/', '')
                currency = Currency.get_currency(currency_name)
                if currency is None:
                    continue
                rate = convert_to_float(values[1].strip())
                if rate is not None:
                    transfer_rate = ExchangeRate(currency.code, rate)
                    transfer_rates.append(transfer_rate)

    company_exchange_rates = CompanyExchangeRates(transfer_rates)
    company_exchange_rates.set_current_scrape_date()
    company_exchange_rates.set_exchange_type(ExchangeType.TRANSFER)
    return company_exchange_rates


def scrape_al_dahab_exchange() -> ExchangeCompany | None:
    try:
        company_exchange_rates = scrape_al_dahab_exchange_rates()

        if company_exchange_rates is None:
            return None

        exchange_company = ExchangeCompany(ExchangeBusinessNames.AL_DAHAB_EXCHANGE,
                                           ExchangeBusinessUrl.AL_DAHAB_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)
        exchange_company.add_exchange_rate(company_exchange_rates)
        # exchange_company.set_exchange_rates(company_exchange_rates)
        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping ', ExchangeBusinessNames.AL_DAHAB_EXCHANGE, err)
    return None

