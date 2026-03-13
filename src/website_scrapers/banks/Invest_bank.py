import re
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup, PageElement

from src.util.common_classes.company_data import BankName, BankUrl, BankExchangeRateUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, ExchangeRate, Currency, \
    CompanyExchangeRates, ExchangeType, get_currency_code_by_name
from src.util.scraping_util.browser_util import get_website_content_by_browser
from src.util.tool.string_util import convert_to_float, get_element_text, get_element_text_by_index

BUY_RATE = 'We Buy'
SELL_RATE = 'We Sell'
UPDATED_AT_STRING = 'Last updated on:'


def get_table_headers(table_headers: List[PageElement]) -> dict:
    element_index_dict = {

    }

    for i in range(0, len(table_headers)):
        th = table_headers[i]
        if th is not None and th.get_text() is not None:
            th_text = th.get_text().strip().lower()

            if (BUY_RATE.lower() in th_text):
                element_index_dict[BUY_RATE] = i

            elif (SELL_RATE.lower() in th_text):
                element_index_dict[SELL_RATE] = i

    return element_index_dict


def get_update_date(update_date: str) -> datetime | None:
    if update_date != None:
        date_obj = datetime.strptime(update_date, "%m/%d/%Y %I:%M %p")
        return date_obj

    return None

def extract_exchange_from_row_element(table_row: PageElement, table_headers: dict) -> ExchangeRate | None:
    if (table_row is None):
        return

    table_data_list = table_row.find_all('td')

    if (table_data_list is not None):
        currency_name = get_element_text_by_index(table_data_list, 0)
        currency_code = get_currency_code_by_name(currency_name)
        if (currency_code is None):
            return None

        buy_rate = get_element_text(table_data_list, table_headers, BUY_RATE)
        sell_rate = get_element_text(table_data_list, table_headers, SELL_RATE)

        if buy_rate is not None and sell_rate is not None:
            exchange_rate = ExchangeRate(currency_code, convert_to_float(buy_rate),
                                         convert_to_float(sell_rate))
            return exchange_rate
    return None


def extract_exchange_rates_from_table(table: PageElement) -> List[ExchangeRate]:
    thead = table.find('thead')
    exchange_rates = []

    if (thead is not None):
        ths = thead.find_all('th')
        table_headers = get_table_headers(ths)
        tbody = table.find('tbody')

        if (tbody is not None):
            trs = tbody.find_all('tr')
            if (trs is not None):
                for tr in trs:
                    exchange_rate = extract_exchange_from_row_element(tr, table_headers)
                    if exchange_rate is not None:
                       exchange_rates.append(exchange_rate)

    return exchange_rates


def get_rates_from_invest_bank():
    content = get_website_content_by_browser(BankExchangeRateUrl.INVEST_BANK,10)
    if (content is not None):
        soup = BeautifulSoup(content, 'html.parser')
        if (soup is not None):
            table = soup.select_one('.FXRatesList table')
            if table is not None:
                exchange_rates = extract_exchange_rates_from_table(table)
                company_exchange_rates = CompanyExchangeRates(exchange_rates)
                company_exchange_rates.set_current_scrape_date()

                company_exchange_rates.set_exchange_type(ExchangeType.CASH)
                return company_exchange_rates

    return None


def scrape_invest_bank() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_invest_bank()
        exchange_company = ExchangeCompany(BankName.INVEST_BANK,
                                           BankUrl.INVEST_BANK,
                                           ExchangeCompanyType.NATIONAL_BANK)
        exchange_company.add_exchange_rate(company_exchange_rates)
        return exchange_company

    except Exception as err:
        # TODO log this
         print('Error while scraping ', BankName.INVEST_BANK, err)