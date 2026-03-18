import re
from typing import List

from bs4 import BeautifulSoup, PageElement

from src.util.common_classes.company_data import ExchangeBusinessNames, ExchangeBusinessExchangeUrl, \
    ExchangeBusinessUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, ExchangeRate, Currency, \
    CompanyExchangeRates, ExchangeType
from src.util.scraping_util.request_util import make_get_request_with_proxy
from src.util.tool.string_util import convert_to_float, get_element_text_by_index, convert_to_reverse_float

CURRENCY = 'Currency'
TRANSFER_RATE = 'Transfer'
CASH_BUY_RATE = 'Buying'
CASH_SELL_RATE = 'Selling'
CASH = 'Cash'
TRANSFER = 'Transfer'


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

                if (TRANSFER_RATE.lower() in th_text):
                    element_index_dict[TRANSFER_RATE] = i

                elif (CASH_BUY_RATE.lower() in th_text):
                    element_index_dict[CASH_BUY_RATE] = i

                elif (CASH_SELL_RATE.lower() in th_text):
                    element_index_dict[CASH_SELL_RATE] = i

    return element_index_dict


def clean_rate(rate: str):
    if rate is not None:
        return rate.replace("AED", '').replace('aed', '').strip()
    return None


def extract_exchange_from_row_element(table_row: PageElement, table_headers: dict) -> dict | None:
    if (table_row is None):
        return

    table_data_list = table_row.find_all('td')
    table_currency_header = table_row.find_all('th')
    exchange_dict = {

    }

    if (table_data_list is not None and table_currency_header is not None):
        currency_code = get_element_text_by_index(table_currency_header, 0)
        currency = Currency.get_currency(currency_code)

        if (currency is not None):
            cash_buy_rate = get_element_text_by_index(table_data_list, table_headers[CASH_BUY_RATE] - 1)
            cash_sell_rate = get_element_text_by_index(table_data_list, table_headers[CASH_SELL_RATE] - 1)

            transfer_rate = get_element_text_by_index(table_data_list, table_headers[TRANSFER_RATE] - 1)

            if cash_buy_rate is not None and cash_sell_rate is not None:
                cash_buy_rate = convert_to_float(clean_rate(cash_buy_rate))
                cash_sell_rate = convert_to_float(clean_rate(cash_sell_rate))
                if cash_sell_rate <= 0:
                    cash_sell_rate = None

                if cash_buy_rate <= 0:
                    cash_buy_rate = None

                cash_exchange_rate = ExchangeRate(currency.code, convert_to_float(cash_buy_rate),
                                                  convert_to_float(cash_sell_rate))
                exchange_dict[CASH] = cash_exchange_rate

            # reverse
            if transfer_rate is not None:
                transfer_rate = clean_rate(transfer_rate)
                transfer_rate_float = convert_to_reverse_float(transfer_rate)

                if (transfer_rate_float > 0):

                    exchange_rate = ExchangeRate(currency.code, rate=transfer_rate_float)
                    exchange_rate.set_original_rate(convert_to_float(transfer_rate))
                    exchange_dict[TRANSFER] = exchange_rate

    return exchange_dict


def get_rates_from_al_fuade() -> List[CompanyExchangeRates] | None:
    content = make_get_request_with_proxy(ExchangeBusinessExchangeUrl.AL_FUAD_EXCHANGE)
    if (content is None):
        return None
    html_page = BeautifulSoup(content, 'html.parser')

    if (html_page is None):
        return None
    table = html_page.find('table')

    if table is None:
        return None
    headers = get_table_headers(table)

    if headers is None:
        return None

    tbody = table.find('tbody')
    transfer_exchange_rates = []
    cash_exchange_rates = []

    if (tbody is not None):
        trs = tbody.find_all('tr')
        if (trs is not None):
            for tr in trs:
                exchange_rates_dict = extract_exchange_from_row_element(tr, headers)

                if CASH in exchange_rates_dict:
                    cash_exchange_rates.append(exchange_rates_dict[CASH])

                if TRANSFER in exchange_rates_dict:
                    transfer_exchange_rates.append(exchange_rates_dict[TRANSFER])

    cash_exchange_rates = CompanyExchangeRates(cash_exchange_rates)
    cash_exchange_rates.set_exchange_type(ExchangeType.CASH)
    cash_exchange_rates.set_current_scrape_date()

    transfer_exchange_rates = CompanyExchangeRates(transfer_exchange_rates)
    transfer_exchange_rates.set_exchange_type(ExchangeType.TRANSFER)
    transfer_exchange_rates.set_current_scrape_date()

    exchange_rates = []
    exchange_rates.append(cash_exchange_rates)
    exchange_rates.append(transfer_exchange_rates)
    return exchange_rates


def scrape_al_fuade() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_al_fuade()
        if (company_exchange_rates is None):
            return None
        exchange_company = ExchangeCompany(ExchangeBusinessNames.AL_FUAD_EXCHANGE,
                                           ExchangeBusinessUrl.AL_FUAD_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)

        exchange_company.set_exchange_rates(company_exchange_rates)

        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping ', ExchangeBusinessNames.AL_FUAD_EXCHANGE, err)
    return None
