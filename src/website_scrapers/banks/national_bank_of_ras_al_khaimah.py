from bs4 import BeautifulSoup

from src.util.common_classes.company_data import BankName, BankUrl, BankExchangeRateUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType
from src.util.scraping_util.request_util import make_get_request_with_proxy



def extract_excluded_rates():
    content = make_get_request_with_proxy(BankExchangeRateUrl.NATIONAL_BANK_OF_RAS_AL_KHAIMAH)
    soup = BeautifulSoup(content, 'html.parser')
    json_script = soup.find('script', id='__NEXT_DATA__')

    if json_script is not None:
        json_data = json.loads(json_script.string.strip())
        if SITECORE in json_data and ROUTE in json_data[SITECORE]:
            return json_data

def get_rates_from_national_bank_of_ras_al_khaimah():
    return None


def scrape_national_bank_of_ras_al_khaimah() -> ExchangeCompany | None:
    try:
        raw_rates = get_rates_from_national_bank_of_ras_al_khaimah()
        # company_exchange_rates = parse_rates(raw_rates)
        exchange_company = ExchangeCompany(BankName.NATIONAL_BANK_OF_RAS_AL_KHAIMAH,
                                           BankUrl.NATIONAL_BANK_OF_RAS_AL_KHAIMAH,
                                           ExchangeCompanyType.NATIONAL_BANK)
        # exchange_company.set_exchange_rates(company_exchange_rates)
        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping emirates islamic bank data', err)
    return None
