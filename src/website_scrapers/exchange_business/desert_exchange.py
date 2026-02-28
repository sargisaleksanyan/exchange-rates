from datetime import datetime
from typing import List

from bs4 import BeautifulSoup, PageElement
from src.util.common_classes.company_data import ExchangeBusinessNames, \
    ExchangeBusinessUrl, ExchangeBusinessExchangeUrl
from src.util.common_classes.exchange_company import ExchangeCompany, CompanyExchangeRates, \
    ExchangeCompanyType, Currency, ExchangeRate, ExchangeType
from src.util.scraping_util.request_util import make_get_request_with_proxy
from src.util.tool.string_util import convert_to_float, convert_to_reverse_float, get_element_text

CURRENCY_HEAD = 'Code'
BANK_TRANSFER = 'Bank Transfer'
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


def extract_desert_exchange_rates(url) -> CompanyExchangeRates:
    content = make_get_request_with_proxy(url)

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
            currency_code = get_element_text(table_data_elements, table_headers, CURRENCY_HEAD)
            currency = Currency.get_currency(currency_code)

            if currency_code is not None and Currency.get_currency(
                    currency_code) is not None:

                if (BANK_TRANSFER in table_headers):
                    transfer_rate = get_element_text(table_data_elements, table_headers, BANK_TRANSFER)
                    if (transfer_rate is not None):
                        transfer_rate_number = convert_to_float(transfer_rate)
                        if transfer_rate_number is not None and transfer_rate_number > 0:
                            exchange_rate = ExchangeRate(currency.code, rate=convert_to_reverse_float(transfer_rate))
                            exchange_rate.set_original_rate(transfer_rate_number)
                            exchange_rates.append(exchange_rate)

                elif BUY_RATE_HEAD in table_headers:
                    buy_rate = get_element_text(table_data_elements, table_headers, BUY_RATE_HEAD)
                    sell_rate = get_element_text(table_data_elements, table_headers, SELL_RATE_HEAD)

                    buy = convert_to_float(buy_rate)
                    sell = convert_to_float(sell_rate)

                    if buy > 0 and sell > 0:
                        exchange_rate = ExchangeRate(currency.code, buy, sell)
                        exchange_rates.append(exchange_rate)

    company_exchange_rates = CompanyExchangeRates(exchange_rates)
    company_exchange_rates.set_current_scrape_date()
    return company_exchange_rates


def extract_desert_exchange_all_rates() -> List[CompanyExchangeRates]:
    cash_exchange_rates = extract_desert_exchange_rates(ExchangeBusinessExchangeUrl.DESERT_EXCHANGE)
    cash_exchange_rates.set_current_scrape_date()
    cash_exchange_rates.set_exchange_type(ExchangeType.CASH)

    transfer_exchange_rates = extract_desert_exchange_rates(ExchangeBusinessExchangeUrl.DESERT_EXCHANGE_TRANSFER)
    cash_exchange_rates.set_current_scrape_date()
    transfer_exchange_rates.set_exchange_type(ExchangeType.TRANSFER)
    return [cash_exchange_rates, transfer_exchange_rates]


def scrape_desert_exchange() -> ExchangeCompany | None:
    try:
        company_exchange_rates = extract_desert_exchange_all_rates()
        exchange_company = ExchangeCompany(ExchangeBusinessNames.DESERT_EXCHANGE, ExchangeBusinessUrl.DESERT_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)
        exchange_company.set_exchange_rates(company_exchange_rates)
        return exchange_company

    except Exception as err:
        print('Error occurred while scraping ', ExchangeBusinessNames.DESERT_EXCHANGE, err)
    return None
