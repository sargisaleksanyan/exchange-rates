import re
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup, PageElement
from src.util.common_classes.company_data import BankName, BankUrl, BankExchangeRateUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, Currency, ExchangeRate, \
    CompanyExchangeRates, ExchangeType
from src.util.scraping_util.browser_util import get_website_content_by_browser
from src.util.tool.string_util import convert_to_float

CURRENCY_CODE = 'Currency'
BUY_RATE = 'Buy Rate'
SELL_RATE = 'Sell Rate'
UPDATED_AT_STRING = 'Updated at:'

def get_update_date(update_date: str) -> datetime | None:
    if update_date != None:
        date_obj = datetime.strptime(update_date, "%Y-%m-%d %H:%M:%S")
        return date_obj

    return None


def get_element_text(td_elements, index: int):
    if (td_elements is not None and len(td_elements) > index):
        element = td_elements[index]
        if (element is not None):
            value = element.get_text().strip()
            return value

    return None


def get_table_headers(table_headers: List[PageElement]) -> dict:
    element_index_dict = {

    }

    for i in range(0, len(table_headers)):
        th = table_headers[i]
        if th is not None and th.get_text() is not None:
            th_text = th.get_text().strip()

            if (th_text == CURRENCY_CODE or CURRENCY_CODE.lower() in th_text.lower()):
                element_index_dict[CURRENCY_CODE] = i

            elif (th_text == BUY_RATE or BUY_RATE.lower() in th_text.lower()):
                element_index_dict[BUY_RATE] = i

            elif (th_text == SELL_RATE or SELL_RATE.lower() in th_text.lower()):
                element_index_dict[SELL_RATE] = i

    return element_index_dict


def extract_exchange_from_row_element(table_row: PageElement, table_headers: dict) -> ExchangeRate | None:
    if (table_row is None):
        return

    table_data_list = table_row.find_all('td')

    if (table_data_list is not None):
        currency_code = get_element_text(table_data_list, table_headers[CURRENCY_CODE])
        currency = Currency.get_currency(currency_code)

        if (currency is not None):
            buy_rate = get_element_text(table_data_list, table_headers[BUY_RATE])
            sell_rate = get_element_text(table_data_list, table_headers[SELL_RATE])

            if buy_rate is not None and sell_rate is not None:
                exchange_rate = ExchangeRate(currency.code, convert_to_float(buy_rate),
                                             convert_to_float(sell_rate))  # handle this case
                return exchange_rate

    return None


def find_update_date(soup: BeautifulSoup):
    updated_at_element = soup.find("p", string=re.compile(r"Updated at:"))

    if updated_at_element is not None:
        updated_at_text = updated_at_element.get_text()
        if updated_at_text is not None:
            updated_at_text = updated_at_text.replace(UPDATED_AT_STRING, "").strip()
            updated_at = get_update_date(updated_at_text)
            return updated_at

    return None


def get_rates_from_commercial_bank_of_dubai():
    content = get_website_content_by_browser(BankExchangeRateUrl.COMMERCIAL_BANK_OF_DUBAI)
    soup = BeautifulSoup(content, 'html.parser')
    tables = soup.find_all(class_='custom-table')
    exchange_rates = []

    if tables is not None and len(tables) > 0:
        for table in tables:
            thead = table.find('thead')
            tbody = table.find('tbody')
            if (
                    thead is not None and tbody is not None and thead.get_text() is not None and 'Currency' in thead.get_text() and 'Buy Rate' in thead.get_text()):
                ths = thead.find_all('th')

                table_headers = get_table_headers(ths)
                table_rows = tbody.find_all('tr')

                if table_rows is not None and len(table_rows) > 0:
                    for table_row in table_rows:
                        if (table_row is not None):
                            exchange_rate = extract_exchange_from_row_element(table_row, table_headers)
                            if exchange_rate is not None:
                                exchange_rates.append(exchange_rate)

    company_exchange_rates = CompanyExchangeRates(exchange_rates)
    company_exchange_rates.set_exchange_type(ExchangeType.TRANSFER)
    company_exchange_rates.set_current_scrape_date()
    update_date = find_update_date(soup)

    if update_date is not None:
        company_exchange_rates.set_update_date(update_date)

    return company_exchange_rates


def scrape_commercial_bank_of_dubai() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_commercial_bank_of_dubai()
        exchange_company = ExchangeCompany(BankName.COMMERCIAL_BANK_OF_DUBAI,
                                           BankUrl.COMMERCIAL_BANK_OF_DUBAI,
                                           ExchangeCompanyType.NATIONAL_BANK)
        exchange_company.add_exchange_rate(company_exchange_rates)
        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping emirates islamic bank data', err)
    return None
