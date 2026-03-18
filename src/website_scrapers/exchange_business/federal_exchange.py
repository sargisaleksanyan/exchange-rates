# exchange-mny-tab-content
from src.util.common_classes.company_data import ExchangeBusinessNames, ExchangeBusinessUrl, ExchangeBusinessExchangeUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, CompanyExchangeRates, \
    Currency, ExchangeRate, ExchangeType
from src.util.scraping_util.request_util import make_get_request_with_parsed_html
from src.util.tool.string_util import convert_to_float, is_float_ok, convert_to_reverse_float


def scrape_federal_exchange_rates() -> CompanyExchangeRates | None:
    html = make_get_request_with_parsed_html(ExchangeBusinessExchangeUrl.FEDERAL_EXCHANGE)
    if (html is None):
        return None
    # option_elements = html.select('․option_currency')
    currency_rate_elements = html.select(".currency-rate")

    transfer_rates = []

    if currency_rate_elements is not None:
        for currency_rate_element in currency_rate_elements:
            text = currency_rate_element.getText()
            if text is None:
                continue
            values = text.split(' ')
            if len(values) > 1:
                currency_name = values[1].strip()
                currency = Currency.get_currency(currency_name)
                if currency is None:
                    continue
                code = currency.code

                rate_text = values[0].strip()
                rate = convert_to_float(rate_text)

                if is_float_ok(rate) == True:

                    if (code == 'USD' and rate > 1):
                        transfer_rate = ExchangeRate(code, rate=convert_to_reverse_float(rate_text))
                        transfer_rate.set_original_rate(rate)
                        transfer_rates.append(transfer_rate)
                    else:
                        transfer_rate = ExchangeRate(code, rate=rate)
                        transfer_rates.append(transfer_rate)

    company_exchange_rates = CompanyExchangeRates(transfer_rates)
    company_exchange_rates.set_current_scrape_date()
    company_exchange_rates.set_exchange_type(ExchangeType.TRANSFER)
    return company_exchange_rates


def scrape_federal_exchange() -> ExchangeCompany | None:
    try:
        company_exchange_rates = scrape_federal_exchange_rates()

        if company_exchange_rates is None:
            return None

        exchange_company = ExchangeCompany(ExchangeBusinessNames.FEDERAL_EXCHANGE,
                                           ExchangeBusinessUrl.FEDERAL_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)
        exchange_company.add_exchange_rate(company_exchange_rates)
        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping ', ExchangeBusinessNames.FEDERAL_EXCHANGE, err)
    return None
