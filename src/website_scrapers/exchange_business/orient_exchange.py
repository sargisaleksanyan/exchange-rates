from src.util.common_classes.company_data import ExchangeBusinessNames, ExchangeBusinessExchangeUrl, \
    ExchangeBusinessApiUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType
from src.util.scraping_util.request_util import make_get_request_with_proxy


def get_rates_from_orient_exchange():
    cash_buy_rates = make_get_request_with_proxy(ExchangeBusinessApiUrl.ORIENT_EXCHANGE_BUY_RATES)
    cash_sell_rates = make_get_request_with_proxy(ExchangeBusinessApiUrl.ORIENT_EXCHANGE_SELL_RATES)
    tranfer_rates = make_get_request_with_proxy(ExchangeBusinessApiUrl.ORIENT_EXCHANGE_TRANSFER)
    m = 5


def scrape_orient_exchange() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_orient_exchange()
        exchange_company = ExchangeCompany(ExchangeBusinessNames.ORIENT_EXCHANGE,
                                           ExchangeBusinessExchangeUrl.ORIENT_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)

        exchange_company.add_exchange_rate(company_exchange_rates)

        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping emirates islamic bank data', err)
    return None

scrape_orient_exchange()