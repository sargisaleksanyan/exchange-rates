from datetime import datetime
from typing import List

from bs4 import BeautifulSoup, PageElement

from src.util.common_classes.company_data import BankName, BankUrl, BankExchangeRateUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, ExchangeRate, Currency, \
    CompanyExchangeRates, ExchangeType
from src.util.scraping_util.request_util import  make_get_request_with_proxy
from src.util.tool.string_util import convert_to_float, get_element_text

CURRENCY_CODE = 'CURRENCY CODE'
BUY_RATE = 'BUYING'
SELL_RATE = 'SELLING'
UPDATED_AT_STRING = 'Last updated on the'


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

            elif (CURRENCY_CODE.lower() in th_text):
                element_index_dict[CURRENCY_CODE] = i


    return element_index_dict


def get_update_date(update_date: str) -> datetime | None:
    try:
        if update_date != None:
            return datetime.strptime(update_date.split(" GMT")[0], "%b %d, %Y %H:%M")
    except Exception as err:
        print('Error', err)
    return None


def find_update_date(soup: BeautifulSoup):
    updated_at_element = soup.find(class_='updatestatus')

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
        currency_code = get_element_text(table_data_list, table_headers,CURRENCY_CODE)
        if (currency_code is not None):
            currency_strings = currency_code.split('-')
            if len(currency_strings) > 0:
                currency_code = currency_strings[0].strip()
        currency = Currency.get_currency(currency_code)

        if (currency is not None):
            buy_rate = get_element_text(table_data_list, table_headers, BUY_RATE)
            sell_rate = get_element_text(table_data_list, table_headers, SELL_RATE)

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


def get_rates_from_bank_of_barodauae():
    content = make_get_request_with_proxy(BankExchangeRateUrl.BANK_OF_BARODAUAE,verify=False)

    if (content is not None):

        soup = BeautifulSoup(content, 'html.parser')
        if soup is None:
            return
        table = soup.find(class_='tableData')
        if table is not None:
            exchange_rates = extract_exchange_rates_from_table(table)
            company_exchange_rates = CompanyExchangeRates(exchange_rates)
            company_exchange_rates.set_current_scrape_date()
            update_date = find_update_date(soup)

            if (update_date is not None):
                company_exchange_rates.set_update_date(update_date)
            company_exchange_rates.set_exchange_type(
                ExchangeType.CASH)  # TODO from there website it is not clear if exchange rate is for transfer or cash
            return company_exchange_rates

    return None


def scrape_bank_of_barodauae() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_bank_of_barodauae()
        exchange_company = ExchangeCompany(BankName.BANK_OF_BARODAUAE,
                                           BankUrl.BANK_OF_BARODAUAE,
                                           ExchangeCompanyType.NATIONAL_BANK)
        exchange_company.add_exchange_rate(company_exchange_rates)
        return exchange_company

    except Exception as err:
        # TODO log this
        print('Error while scraping ', BankName.BANK_OF_BARODAUAE, err)

