from src.util.common_classes.company_data import ExchangeBusinessNames, ExchangeBusinessExchangeUrl
from src.util.common_classes.exchange_company import ExchangeCompany, CompanyExchangeRates, ExchangeCompanyType


def get_rates_from_joyalukkas():CompanyExchangeRates | None

def scrape_joyalukkas_exchange() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_joyalukkas()
        # company_exchange_rates = parse_rates(raw_rates)
        exchange_company = ExchangeCompany(ExchangeBusinessNames.JOYALUKKAS_EXCHANGE,
                                           ExchangeBusinessExchangeUrl.JOYALUKKAS_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)
        exchange_company.add_exchange_rate(company_exchange_rates)
        # exchange_company.set_exchange_rates(company_exchange_rates)
        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping emirates islamic bank data', err)
    return None