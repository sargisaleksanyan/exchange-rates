import re
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup, PageElement
from src.util.common_classes.company_data import ExchangeBusinessNames, \
    ExchangeBusinessUrl, ExchangeBusinessExchangeUrl
from src.util.common_classes.exchange_company import ExchangeCompany, CompanyExchangeRates, \
    ExchangeCompanyType, Currency, ExchangeRate, ExchangeType
from src.util.scraping_util.request_util import make_get_request_with_proxy
from src.util.tool.string_util import convert_to_float

TRANSFER_RATE = 'Remittance Transfer Rate'  # TODO Remittances is not taken as it contains incorrect data
CURRENCY_CODE_HEAD = 'Currency code'
CURRENCY_RATE = 'Currency Rate'
BUY_RATE_HEAD = 'Buying Rate'
SELL_RATE_HEAD = 'Selling'

UPDATED_AT_STRING = 'Last Updated / Time:'


def get_table_headers(page_element: PageElement) -> dict:
    thead = page_element.find('thead')

    if thead is None:
        return {}

    # TODO headers are hardcoded , need to change it later

    return {
        CURRENCY_CODE_HEAD: 2,
        BUY_RATE_HEAD: 3,
        SELL_RATE_HEAD: 4,
        TRANSFER_RATE: 5
    }


def get_element_text(td_elements, index: int):
    if (td_elements is not None and len(td_elements) > index):
        element = td_elements[index]
        if (element is not None):
            value = element.get_text().strip()
            return value

    return None


def get_update_date(update_date: str) -> datetime | None:
    if update_date != None:
        date_obj = datetime.strptime(update_date, "%d %B %Y %I:%M %p")
        return date_obj

    return None


def extract_dar_exchange_rates() -> List[CompanyExchangeRates] | None:
    content = make_get_request_with_proxy(ExchangeBusinessExchangeUrl.DAR_EXCHANGE)

    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table')
    table_headers = get_table_headers(table)

    if (table is None):
        return None

    tbody = table.find('tbody')
    if tbody is None:
        return None

    table_rows = tbody.find_all('tr')

    if table_rows is None or len(table_rows) == 0:
        return None

    exchange_rates = []
    transfer_rates = []

    for table_row in table_rows:
        table_data_elements = table_row.find_all('td')
        if table_data_elements is not None and len(table_data_elements) > 0:
            currency_code = get_element_text(table_data_elements, table_headers[CURRENCY_CODE_HEAD])
            buy_rate = get_element_text(table_data_elements, table_headers[BUY_RATE_HEAD])
            sell_rate = get_element_text(table_data_elements, table_headers[SELL_RATE_HEAD])
            transfer_rate = get_element_text(table_data_elements, table_headers[TRANSFER_RATE])

            if currency_code is not None and Currency.get_currency(
                    currency_code) is not None:

                currency = Currency.get_currency(currency_code)

                if buy_rate is not None and sell_rate is not None:
                    buy = convert_to_float(buy_rate)
                    sell = convert_to_float(sell_rate)
                    try:
                        if buy is not None and sell is not None and buy > 0 and sell > 0 and sell >= buy:
                            exchange_rate = ExchangeRate(currency.code, buy_rate=buy, sell_rate=sell)
                            exchange_rates.append(exchange_rate)
                    except Exception as err:
                        print('Error occurred while scraping ', ExchangeBusinessNames.DAR_EXCHANGE, err)

                if transfer_rate is not None and convert_to_float(transfer_rate) is not None:
                    exchange_rate = ExchangeRate(currency.code, rate=convert_to_float(transfer_rate))
                    transfer_rates.append(exchange_rate)

    company_exchange_rates = CompanyExchangeRates(exchange_rates)
    company_exchange_rates.set_current_scrape_date()
    company_exchange_rates.set_exchange_type(ExchangeType.CASH)

    company_transfer_rates = CompanyExchangeRates(transfer_rates)
    company_transfer_rates.set_current_scrape_date()
    company_exchange_rates.set_exchange_type(ExchangeType.TRANSFER)
    return [company_exchange_rates, company_transfer_rates]


def scrape_dar_exchange() -> ExchangeCompany | None:
    try:
        company_exchange_rates = extract_dar_exchange_rates()
        exchange_company = ExchangeCompany(ExchangeBusinessNames.DAR_EXCHANGE, ExchangeBusinessUrl.DAR_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)
        exchange_company.set_exchange_rates(company_exchange_rates)
        return exchange_company

    except Exception as err:
        print('Error occurred while scraping ', ExchangeBusinessNames.DAR_EXCHANGE, err)
    return None


scrape_dar_exchange()
