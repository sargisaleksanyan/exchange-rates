from bs4 import BeautifulSoup

from src.util.common_classes.company_data import ExchangeBusinessNames, ExchangeBusinessExchangeUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType
from src.util.scraping_util.request_util import make_get_request_with_proxy


def get_rates_from_al_ansari():
    content = make_get_request_with_proxy(ExchangeBusinessExchangeUrl.AL_ANSARI_EXCHANGE)

    if content is not None:
        soup = BeautifulSoup(content, 'html.parser')
        currency_wrapper = soup.find(class_='currency-select')
        if currency_wrapper is not None:
            currency_list = currency_wrapper.find_all('li')


def scrape_al_ansari_exchange() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_al_ansari()
        # company_exchange_rates = parse_rates(raw_rates)
        exchange_company = ExchangeCompany(ExchangeBusinessNames.AL_ANSARI_EXCHANGE,
                                           ExchangeBusinessExchangeUrl.JOYALUKKAS_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)
        exchange_company.add_exchange_rate(company_exchange_rates)
        # exchange_company.set_exchange_rates(company_exchange_rates)
        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping emirates islamic bank data', err)
    return None
