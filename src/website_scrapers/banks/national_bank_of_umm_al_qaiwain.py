import re
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup, PageElement

from src.util.common_classes.company_data import BankName, BankUrl, BankExchangeRateUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, ExchangeRate, Currency, \
    CompanyExchangeRates
from src.util.scraping_util.request_util import make_get_request_with_proxy
from src.util.tool.string_util import convert_to_float

CURRENCY_EXCHANGE_RATES = 'Currency Exchange Rates'
BUY_RATE = 'Buy'
SELL_RATE = 'Sell'
UPDATED_AT_STRING = 'Last updated on:'


def get_table_headers(table_headers: List[PageElement]) -> dict:
    element_index_dict = {

    }

    for i in range(0, len(table_headers)):
        th = table_headers[i]
        if th is not None and th.get_text() is not None:
            th_text = th.get_text().strip().lower()

            if (CURRENCY_EXCHANGE_RATES.lower() in th_text):
                element_index_dict[CURRENCY_EXCHANGE_RATES] = i

            elif (BUY_RATE.lower() in th_text):
                element_index_dict[BUY_RATE] = i

            elif (SELL_RATE.lower() in th_text):
                element_index_dict[SELL_RATE] = i

    return element_index_dict


def get_element_text(td_elements, index: int):
    if (td_elements is not None and len(td_elements) > index):
        element = td_elements[index]
        if (element is not None):
            value = element.get_text().strip()
            return value

    return None


def get_update_date(update_date: str) -> datetime | None:
    if update_date != None:
        date_obj = datetime.strptime(update_date, "%m/%d/%Y %I:%M %p")
        return date_obj

    return None


def find_update_date(soup: BeautifulSoup):
    # updated_at_element = soup.find("p", string=re.compile(r"Last updated on"))
    updated_at_element = soup.find(string=re.compile(r"Last updated on"))

    if updated_at_element is not None:
        updated_at_text = updated_at_element.get_text()
        if updated_at_text is not None:
            updated_at_text = updated_at_text.replace(UPDATED_AT_STRING, "").replace("\n", "").replace("\r",
                                                                                                       "").replace(
                "Date:", "").replace("Time:", "").replace("  ", " ").strip()
            updated_at = get_update_date(updated_at_text)
            return updated_at

    return None


def extract_exchange_from_row_element(table_row: PageElement, table_headers: dict) -> ExchangeRate | None:
    if (table_row is None):
        return

    table_data_list = table_row.find_all('td')

    if (table_data_list is not None):
        currency_code = get_element_text(table_data_list, table_headers[CURRENCY_EXCHANGE_RATES])
        if (currency_code is not None):
            currency_strings = currency_code.split('-')
            if len(currency_strings) > 0:
                currency_code = currency_strings[0].strip()
        currency = Currency.get_currency(currency_code)

        if (currency is not None):
            buy_rate = get_element_text(table_data_list, table_headers[BUY_RATE])
            sell_rate = get_element_text(table_data_list, table_headers[SELL_RATE])

            if buy_rate is not None and sell_rate is not None:
                exchange_rate = ExchangeRate(currency.code, convert_to_float(buy_rate),
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
                    exchange_rates.append(exchange_rate)

    return exchange_rates


def get_rates_from_national_bank_of_umm_al_qaiwain():
    content = make_get_request_with_proxy(BankExchangeRateUrl.NATIONAL_BANK_OF_UMM_AL_QAIWAIN)
    if (content is not None):
        soup = BeautifulSoup(content, 'html.parser')
        if (soup is not None):
            table = soup.find(class_='currency-rates-table')
            if table is not None:
                exchange_rates = extract_exchange_rates_from_table(table)
                company_exchange_rates = CompanyExchangeRates(exchange_rates)
                company_exchange_rates.set_current_scrape_date()
                update_date = find_update_date(soup)

                if (update_date is not None):
                    company_exchange_rates.set_update_date(update_date)
                return company_exchange_rates

    return None


def scrape_national_bank_of_umm_al_qaiwain() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_national_bank_of_umm_al_qaiwain()
        exchange_company = ExchangeCompany(BankName.NATIONAL_BANK_OF_UMM_AL_QAIWAIN,
                                           BankUrl.NATIONAL_BANK_OF_UMM_AL_QAIWAIN,
                                           ExchangeCompanyType.NATIONAL_BANK)
        exchange_company.add_exchange_rate(company_exchange_rates)
        return exchange_company

    except Exception as err:
        # TODO log this
        print('Error while scraping emirates islamic bank data', err)
