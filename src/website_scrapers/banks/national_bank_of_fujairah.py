from bs4 import BeautifulSoup

from src.util.common_classes.company_data import BankName, BankUrl, BankExchangeRateUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, CompanyExchangeRates
from src.util.scraping_util.browser_util import get_website_content_by_browser
from src.util.tool.json_util import parse_string_to_json

WINDOWS_CURRENCY_DATA = 'window.currencyData ='

# TODO
def get_rates_from_national_bank_of_fujairah() -> CompanyExchangeRates | None:
    content = get_website_content_by_browser(BankExchangeRateUrl.NATIONAL_BANK_OF_FUJARAH, wait_time=10)

    if content is not None:
        soup = BeautifulSoup(content, 'html.parser')
        json_scripts = soup.find_all('script')
        for json_script in json_scripts:
            if (json_script is not None and json_script.string is not None):
                json_string = json_script.string

                if 'currencyData' in json_string:
                    json_string = json_script.replace_with(WINDOWS_CURRENCY_DATA, '')
                    if json_string.endswith(';'):
                        json_string = json_script[0, len(json_string) - 2]

                        json_object = parse_string_to_json(json_string)
                        m = 5

    return None


def scrape_national_bank_of_fujairah() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_national_bank_of_fujairah()
        # company_exchange_rates = parse_rates(raw_rates)
        exchange_company = ExchangeCompany(BankName.NATIONAL_BANK_OF_FUJARAH,
                                           BankUrl.NATIONAL_BANK_OF_FUJARAH,
                                           ExchangeCompanyType.NATIONAL_BANK)
        exchange_company.add_exchange_rate(company_exchange_rates)
        # exchange_company.set_exchange_rates(company_exchange_rates)
        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping emirates islamic bank data', err)
    return None


