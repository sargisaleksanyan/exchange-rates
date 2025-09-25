from datetime import datetime

from bs4 import BeautifulSoup, PageElement
from src.util.common_classes.company_data import BankExchangeRateUrl, BankName, BankUrl
from src.util.common_classes.exchange_company import ExchangeCompany, CompanyExchangeRates, ExchangeRate, Currency, \
    ExchangeCompanyType
from src.util.scraping_util.browser_util import get_website_content_by_browser
from src.util.tool.string_util import convert_to_float

CURRENCY_CODE = 'Currency Code'
CURRENCY_SELL = 'Sell'
CURRENCY_BUY = 'Buy'

BUY_RATE_HEADER = 'Buy Rate (AED)'
SELL_RATE_HEADER = 'Sell Rate (AED)'


def get_element_text(td_elements, index: int):
    if (td_elements is not None and len(td_elements) > index):
        element = td_elements[index]
        if (element is not None):
            value = element.get_text().strip()
            return value

    return None


def extract_exchange_rate_from_html(page_element: PageElement):
    element_index_dict = {

    }

    exchange_rates = []
    tr_elements = page_element.find_all('tr')  # you don’t need to re-parse

    for tr_element in tr_elements:
        td_elements = tr_element.find_all('td')
        if td_elements is not None and len(td_elements) > 2:

            if (CURRENCY_CODE not in element_index_dict):
                for i in range(0, len(td_elements)):
                    td = td_elements[i]
                    if td is not None and td.get_text() is not None:

                        td_text = td.get_text().strip().lower()

                        if (td_text == CURRENCY_CODE or CURRENCY_CODE.lower() in td_text.lower()):
                            element_index_dict[CURRENCY_CODE] = i

                        elif (td_text == BUY_RATE_HEADER or 'buy rate' in td_text.lower()):
                            element_index_dict[CURRENCY_SELL] = i

                        elif (td_text == SELL_RATE_HEADER or 'sell rate' in td_text.lower()):
                            element_index_dict[CURRENCY_BUY] = i
            else:
                currency_code = get_element_text(td_elements, element_index_dict[CURRENCY_CODE])

                if currency_code is not None and Currency.get_currency(currency_code) is not None:
                    currency = Currency.get_currency(currency_code)
                    selling = get_element_text(td_elements, element_index_dict[CURRENCY_SELL])
                    buying = get_element_text(td_elements, element_index_dict[CURRENCY_BUY])
                    if (selling is not None and buying is not None):
                        exchangerate = ExchangeRate(currency, convert_to_float(buying), convert_to_float(selling))
                        exchange_rates.append(exchangerate)
                    # exchange_rates.append(exchangerate)
                    # exchange_data =
    return exchange_rates


def extract_update_date(update_date_element):
    if update_date_element is not None:
        value = update_date_element.get('value')
        dt = datetime.strptime(value, "%d-%m-%Y %H:%M")
        return dt
    return None


def extract_company_exchange_rates(content: str) -> CompanyExchangeRates | None:
    soup = BeautifulSoup(content, 'html.parser')
    data_list = soup.find_all(class_='o-comp__content container')
    is_next_element_contains_rates_data = False

    if (data_list is not None):
        for data in data_list:
            if (data is not None):

                if (is_next_element_contains_rates_data == False):

                    if 'Accounts FX Rates'.lower() in data.get_text().lower():
                        is_next_element_contains_rates_data = True

                elif 'Currency Code'.lower() in data.get_text().lower():
                    exchange_rates = extract_exchange_rate_from_html(data)
                    update_date_element = soup.find(id='asoftime')
                    update_date = extract_update_date(update_date_element)  # TODO check this
                    company_exchange_rates = CompanyExchangeRates(exchange_rates)

                    if (update_date is not None):
                        company_exchange_rates.set_update_date(update_date)

                    company_exchange_rates.set_current_scrape_date()
                    return company_exchange_rates

    return None


def scrape_abu_dhabi_commercial_bank() -> ExchangeCompany | None:
    try:
        content = get_website_content_by_browser(BankExchangeRateUrl.ABU_DHABI_COMMERCIAL_BANK)
        company_exchange_rates = extract_company_exchange_rates(content)
        exchange_company = ExchangeCompany(BankName.ABU_DHABI_COMMERCIAL_BANK, BankUrl.ABU_DHABI_COMMERCIAL_BANK,
                                           ExchangeCompanyType.NATIONAL_BANK)
        exchange_company.set_exchange_rates(company_exchange_rates)

        # exchange_company = ExchangeCompany(BankName.FIRST_ABU_DHABI_BANK, BankUrl.FIRST_ABU_DHABI_BANK,
        #                                   ExchangeCompanyType.NATIONAL_BANK)
        # exchange_company.set_exchange_rates(company_exchange_rates)
        return exchange_company
    except Exception as err:
        print('Error occured while scraping ', BankName.ABU_DHABI_COMMERCIAL_BANK, err)
        return None
