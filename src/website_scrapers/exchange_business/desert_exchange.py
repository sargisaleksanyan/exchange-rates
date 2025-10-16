from datetime import datetime
from typing import List

from bs4 import BeautifulSoup, PageElement
from src.util.common_classes.company_data import ExchangeBusinessNames, \
    ExchangeBusinessUrl, ExchangeBusinessExchangeUrl
from src.util.common_classes.exchange_company import ExchangeCompany, CompanyExchangeRates, \
    ExchangeCompanyType, Currency, ExchangeRate
from src.util.scraping_util.request_util import make_get_request_with_proxy
from src.util.tool.string_util import convert_to_float

CURRENCY_HEAD = 'Code'
BUY_RATE_HEAD = 'FC Buy'
SELL_RATE_HEAD = 'Fc Sell'


def get_table_headers(page_element: PageElement) -> dict:
    element_index_dict = {

    }

    table_headers = page_element.find_all('th')

    if table_headers is not None:
        for i in range(0, len(table_headers)):
            th = table_headers[i]
            if th is not None and th.get_text() is not None:
                th_text = th.get_text().strip().lower()

                if (CURRENCY_HEAD.lower() in th_text):
                    element_index_dict[CURRENCY_HEAD] = i

                elif (BUY_RATE_HEAD.lower() in th_text):
                    element_index_dict[BUY_RATE_HEAD] = i

                elif (SELL_RATE_HEAD.lower() in th_text):
                    element_index_dict[SELL_RATE_HEAD] = i

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


def extract_update_date(soup: BeautifulSoup):
    update_date_element = soup.find(id='lDate')

    if update_date_element is not None:
        update_date = update_date_element.get_text()
        if (update_date is not None):
            update_date = update_date.strip()
            date_obj = datetime.strptime(update_date, "%d/%m/%Y")
            return date_obj
    return None


def extract_desert_exchange_rates() -> CompanyExchangeRates:
    content = make_get_request_with_proxy(ExchangeBusinessExchangeUrl.DESERT_EXCHANGE)

    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find(id='exchangerates')
    table_headers = get_table_headers(table)

    if (table is None):
        return None

    table_rows = table.find_all('tr')

    if table_rows is None and len(table_rows) == 0:
        return None

    exchange_rates = []

    for table_row in table_rows:
        table_data_elements = table_row.find_all('td')
        if table_data_elements is not None and len(table_data_elements) > 0:
            currency_code = get_element_text(table_data_elements, table_headers[CURRENCY_HEAD])
            buy_rate = get_element_text(table_data_elements, table_headers[BUY_RATE_HEAD])
            sell_rate = get_element_text(table_data_elements, table_headers[SELL_RATE_HEAD])

            if currency_code is not None and Currency.get_currency(
                    currency_code) is not None and buy_rate is not None and sell_rate is not None:
                currency = Currency.get_currency(currency_code)
                buy = convert_to_float(buy_rate)
                sell = convert_to_float(sell_rate)

                if buy > 0 and sell > 0:
                    exchange_rate = ExchangeRate(currency.code, buy, sell)
                    exchange_rates.append(exchange_rate)

    company_exchange_rates = CompanyExchangeRates(exchange_rates)
    company_exchange_rates.set_current_scrape_date()
    return company_exchange_rates


def scrape_desert_exchange() -> ExchangeCompany | None:
    try:
        company_exchange_rates = extract_desert_exchange_rates()
        exchange_company = ExchangeCompany(ExchangeBusinessNames.DESERT_EXCHANGE, ExchangeBusinessUrl.DESERT_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)
        exchange_company.add_exchange_rate(company_exchange_rates)
        return exchange_company

    except Exception as err:
        print('Error occurred while scraping ', ExchangeBusinessNames.DESERT_EXCHANGE, err)
    return None
