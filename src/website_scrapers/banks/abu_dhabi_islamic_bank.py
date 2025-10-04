from datetime import datetime
from typing import List

from bs4 import BeautifulSoup, PageElement
from src.util.common_classes.company_data import BankExchangeRateUrl, BankName, BankUrl
from src.util.common_classes.exchange_company import ExchangeCompany, CompanyExchangeRates, ExchangeRate, Currency, \
    ExchangeCompanyType, ExchangeType
from src.util.scraping_util.browser_util import get_website_content_by_browser
from src.util.scraping_util.request_util import make_get_request_with_proxy
from src.util.tool.string_util import convert_to_float

CURRENCY_CODE = 'Currency Code'
CURRENCY_SELL = 'Sell'
CURRENCY_BUY = 'Buy'

CASH = 'cash'
TRANSFER = 'transfer'

CURRENCY = 'Currency'
TRANSFER_BUY_RATE = 'Transfer Buy Rate'
TRANSFER_SELL_RATE = 'Transfer Sell Rate'
CASH_BUY_RATE = 'Cash Buy Rate'
CASH_SELL_RATE = 'Cash Sell Rate'
UPDATED_AT_STRING = 'Last updated:'


# def get_table_headers(table_headers: List[PageElement]) -> dict:
def get_table_headers(page_element: PageElement) -> dict:
    element_index_dict = {

    }

    thead = page_element.find('thead')

    if thead is not None:
        table_headers = thead.find_all('th')
        for i in range(0, len(table_headers)):
            th = table_headers[i]
            if th is not None and th.get_text() is not None:
                th_text = th.get_text().strip().lower()

                if (CURRENCY.lower() in th_text):
                    element_index_dict[CURRENCY_CODE] = i

                elif (TRANSFER_BUY_RATE.lower() in th_text):
                    element_index_dict[TRANSFER_BUY_RATE] = i

                elif (TRANSFER_SELL_RATE.lower() in th_text):
                    element_index_dict[TRANSFER_SELL_RATE] = i

                elif (CASH_BUY_RATE.lower() in th_text):
                    element_index_dict[CASH_BUY_RATE] = i

                elif (CASH_SELL_RATE.lower() in th_text):
                    element_index_dict[CASH_SELL_RATE] = i

    return element_index_dict


def get_element_text(td_elements, index: int):
    if (td_elements is not None and len(td_elements) > index):
        element = td_elements[index]
        if (element is not None):
            value = element.get_text().strip()
            return value

    return None


def extract_update_date(update_date_element):
    if update_date_element is not None:
        value = update_date_element.get('value')
        dt = datetime.strptime(value, "%d-%m-%Y %H:%M")
        return dt
    return None


def find_table_from_html(soup: BeautifulSoup):
    table_wrapper_div = soup.find(class_='clsCRRateDiv')
    if table_wrapper_div is not None:
        return table_wrapper_div.find('table')
    return None


def extract_exchange_from_row_element(table_row: PageElement, table_headers: dict) -> dict | None:
    if (table_row is None):
        return

    table_data_list = table_row.find_all('td')
    exchange_dict = {

    }

    if (table_data_list is not None):
        currency_code = get_element_text(table_data_list, table_headers[CURRENCY_CODE])
        currency = Currency.get_currency(currency_code)

        if (currency is not None):
            cash_buy_rate = get_element_text(table_data_list, table_headers[CASH_BUY_RATE])
            cash_sell_rate = get_element_text(table_data_list, table_headers[CASH_SELL_RATE])

            transfer_buy_rate = get_element_text(table_data_list, table_headers[TRANSFER_BUY_RATE])
            transfer_sell_rate = get_element_text(table_data_list, table_headers[TRANSFER_SELL_RATE])

            if cash_buy_rate is not None and cash_sell_rate is not None:
                exchange_rate = ExchangeRate(currency.code, convert_to_float(cash_buy_rate),
                                             convert_to_float(cash_sell_rate))
                exchange_dict[CASH] = exchange_rate

            if transfer_sell_rate is not None and transfer_buy_rate is not None:
                exchange_rate = ExchangeRate(currency.code, convert_to_float(transfer_buy_rate),
                                             convert_to_float(transfer_sell_rate))
                exchange_dict[TRANSFER] = exchange_rate

    return exchange_dict


def extract_update_date(soup: BeautifulSoup):
    update_date_element = soup.find(id='lDate')

    if update_date_element is not None:
        update_date = update_date_element.get_text()
        if (update_date is not None):
            update_date = update_date.strip()
            date_obj = datetime.strptime(update_date, "%d/%m/%Y")
            return date_obj
    return None


def extract_company_exchange_rates() -> List[CompanyExchangeRates] | None:
    content = make_get_request_with_proxy(BankExchangeRateUrl.ABU_DHABI_ISLAMIC_BANK)

    soup = BeautifulSoup(content, 'html.parser')
    table = find_table_from_html(soup)

    table_headers = get_table_headers(table)

    tbody = table.find('tbody')

    cash_exchange_rates = []
    transfer_exchange_rates = []

    if (tbody is not None):
        trs = tbody.find_all('tr')
        if (trs is not None):
            for tr in trs:
                exchange_rates_dict = extract_exchange_from_row_element(tr, table_headers)
                cash_exchange_rate = exchange_rates_dict[CASH]
                transfer_exchange_rate = exchange_rates_dict[TRANSFER]

                if cash_exchange_rate is not None:
                    cash_exchange_rates.append(cash_exchange_rate)

                if transfer_exchange_rate is not None:
                    transfer_exchange_rates.append(transfer_exchange_rate)

    cash_exchange_rates = CompanyExchangeRates(cash_exchange_rates)
    cash_exchange_rates.set_exchange_type(ExchangeType.CASH)
    cash_exchange_rates.set_current_scrape_date()

    transfer_exchange_rates = CompanyExchangeRates(transfer_exchange_rates)
    transfer_exchange_rates.set_exchange_type(ExchangeType.TRANSFER)
    transfer_exchange_rates.set_current_scrape_date()

    update_date = extract_update_date(soup)

    if update_date is not None:
        cash_exchange_rates.set_scrape_date(update_date)
        transfer_exchange_rates.set_scrape_date(update_date)

    exchange_rates = []
    exchange_rates.append(cash_exchange_rates)
    exchange_rates.append(transfer_exchange_rates)
    return exchange_rates


def scrape_abu_dhabi_islamic_bank() -> ExchangeCompany | None:
    try:
        company_exchange_rates = extract_company_exchange_rates()
        exchange_company = ExchangeCompany(BankName.ABU_DHABI_ISLAMIC_BANK, BankUrl.ABU_DHABI_ISLAMIC_BANK,
                                           ExchangeCompanyType.NATIONAL_BANK)
        exchange_company.set_exchange_rates(company_exchange_rates)

        return exchange_company


    except Exception as err:
        print('Error occured while scraping ', BankName.ABU_DHABI_ISLAMIC_BANK, err)
    return None
