import re
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup, PageElement
from src.util.common_classes.company_data import ExchangeBusinessNames, \
    ExchangeBusinessUrl, ExchangeBusinessExchangeUrl
from src.util.common_classes.exchange_company import ExchangeCompany, CompanyExchangeRates, \
    ExchangeCompanyType, Currency, ExchangeRate, ExchangeType
from src.util.scraping_util.request_util import make_get_request_with_proxy
from src.util.tool.string_util import convert_to_float, get_element_text, convert_to_reverse_float, is_float_ok

TRANSFER_HEAD = 'Remittances'  # TODO Remittances is not taken as it contains incorrect data
CURRENCY_HEAD = 'Code'
BUY_RATE_HEAD = 'Buying'
BUY_RATE_HEAD_CASH = 'Buying (Cash)'
SELL_RATE_HEAD = 'Selling'
SELL_RATE_HEAD_CASH = 'Selling (Cash)'
UPDATED_AT_STRING = 'Last Updated / Time:'


def get_table_headers(page_element: PageElement) -> dict:
    element_index_dict = {

    }

    thead = page_element.find('thead')

    if thead is None:
        return element_index_dict

    table_headers = thead.find_all('th')

    if table_headers is not None:
        for i in range(0, len(table_headers)):
            th = table_headers[i]
            if th is not None and th.get_text() is not None:
                th_text = th.get_text().strip().lower()

                if (CURRENCY_HEAD.lower() in th_text):
                    element_index_dict[CURRENCY_HEAD] = i

                elif (BUY_RATE_HEAD.lower() in th_text or BUY_RATE_HEAD_CASH in th_text):
                    element_index_dict[BUY_RATE_HEAD] = i

                elif (SELL_RATE_HEAD.lower() in th_text or SELL_RATE_HEAD_CASH in th_text):
                    element_index_dict[SELL_RATE_HEAD] = i

                elif (TRANSFER_HEAD.lower() in th_text):
                    element_index_dict[TRANSFER_HEAD] = i

    return element_index_dict


def get_update_date(update_date: str) -> datetime | None:
    if update_date != None:
        date_obj = datetime.strptime(update_date, "%d %B %Y %I:%M %p")
        return date_obj

    return None


def find_update_date(soup: BeautifulSoup):
    # updated_at_element = soup.find("p", string=re.compile(r"Last updated on"))
    updated_at_element = soup.find(string=re.compile(r"Last Updated"))

    if updated_at_element is not None:
        updated_at_text = updated_at_element.get_text()
        if updated_at_text is not None:
            updated_at_text = updated_at_text.replace(UPDATED_AT_STRING, "").replace("\n", "").replace("\r",
                                                                                                       "").replace(
                "Date:", "").replace("Time:", "").replace("  ", " ").strip()
            updated_at = get_update_date(updated_at_text)
            return updated_at

    return


def extract_index_exchange_rates() -> List[CompanyExchangeRates] | None:
    content = make_get_request_with_proxy(ExchangeBusinessExchangeUrl.INDEX_EXCHANGE)

    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find(class_='table')
    table_headers = get_table_headers(table)

    if (table is None):
        return None

    tbody = table.find('tbody')
    if tbody is None:
        return None

    table_rows = tbody.find_all('tr')

    if table_rows is None or len(table_rows) == 0:
        return None

    cash_exchange_rates = []
    transfer_exchange_rates = []

    for table_row in table_rows:
        table_data_elements = table_row.find_all('td')
        if table_data_elements is not None and len(table_data_elements) > 0:
            currency_name = get_element_text(table_data_elements, table_headers, CURRENCY_HEAD)
            currency = Currency.get_currency(
                currency_name)

            if (currency is None):
                continue

            transfer_rate_text = get_element_text(table_data_elements, table_headers, BUY_RATE_HEAD)

            if (transfer_rate_text is not None):
                transfer_rate_value = convert_to_reverse_float(transfer_rate_text)

                if is_float_ok(transfer_rate_value) == True:
                    transfer_rate = ExchangeRate(currency.code, rate=transfer_rate_value)
                    transfer_rate.set_original_rate(convert_to_float(transfer_rate_value))
                    transfer_exchange_rates.append(transfer_rate)

            buy = convert_to_float(get_element_text(table_data_elements, table_headers, BUY_RATE_HEAD))
            sell = convert_to_float(get_element_text(table_data_elements, table_headers, SELL_RATE_HEAD))

            if buy is not None and sell is not None and buy > 0 and sell > 0:  # TODO if buy is non but sell has value might accept it
                exchange_rate = ExchangeRate(currency.code, buy, sell)
                cash_exchange_rates.append(exchange_rate)

    company_cash_exchange_rates = CompanyExchangeRates(cash_exchange_rates)
    company_cash_exchange_rates.set_current_scrape_date()
    company_cash_exchange_rates.set_exchange_type(ExchangeType.CASH)

    company_transfer_exchange_rates = CompanyExchangeRates(transfer_exchange_rates)
    company_transfer_exchange_rates.set_current_scrape_date()
    company_transfer_exchange_rates.set_exchange_type(ExchangeType.TRANSFER)

    update_date = find_update_date(soup)

    if update_date is not None:
        company_cash_exchange_rates.set_update_date(update_date)
        company_transfer_exchange_rates.set_update_date(update_date)
    return [company_cash_exchange_rates, company_transfer_exchange_rates]


def scrape_index_exchange() -> ExchangeCompany | None:
    try:
        company_exchange_rates = extract_index_exchange_rates()
        exchange_company = ExchangeCompany(ExchangeBusinessNames.INDEX_EXCHANGE, ExchangeBusinessUrl.INDEX_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)
        exchange_company.set_exchange_rates(company_exchange_rates)
        return exchange_company

    except Exception as err:
        print('Error occurred while scraping ', ExchangeBusinessNames.INDEX_EXCHANGE, err)
    return None
