import re
from typing import List

from bs4 import BeautifulSoup, PageElement

from src.util.common_classes.company_data import ExchangeBusinessNames, ExchangeBusinessExchangeUrl, ExchangeBusinessUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, ExchangeRate, Currency, \
    CompanyExchangeRates, ExchangeType
from src.util.scraping_util.request_util import make_get_request_with_proxy
from src.util.tool.string_util import convert_to_float, get_element_text, convert_to_reverse_float, is_float_ok

CURRENCY = 'CODE'
TRANSFER_RATE = 'T.T RATE'
CASH_BUY_RATE = 'FC BUY'
CASH_SELL_RATE = 'FC SELL'
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

                if (CURRENCY.lower() in th_text):
                    element_index_dict[CURRENCY] = i

                elif (TRANSFER_RATE.lower() in th_text):
                    element_index_dict[TRANSFER_RATE] = i

                elif (CASH_BUY_RATE.lower() in th_text):
                    element_index_dict[CASH_BUY_RATE] = i

                elif (CASH_SELL_RATE.lower() in th_text):
                    element_index_dict[CASH_SELL_RATE] = i

    return element_index_dict


def extract_exchange_from_row_element(table_row: PageElement, table_headers: dict) -> dict | None:
    if (table_row is None):
        return

    table_data_list = table_row.find_all('td')
    exchange_dict = {

    }

    if (table_data_list is not None):
        currency_code = get_element_text(table_data_list, table_headers, CURRENCY)
        currency = Currency.get_currency(currency_code)

        if (
                currency is not None and currency.code != currency.CHF.code):  # TODO in future need to check if in future as for now swiss frank is incorrect
            cash_buy_rate = get_element_text(table_data_list, table_headers, CASH_BUY_RATE)
            cash_sell_rate = get_element_text(table_data_list, table_headers, CASH_SELL_RATE)

            transfer_rate = get_element_text(table_data_list, table_headers, TRANSFER_RATE)

            if cash_buy_rate is not None and cash_sell_rate is not None:
                cash_buy_rate = convert_to_float(cash_buy_rate)
                cash_sell_rate = convert_to_float(cash_sell_rate)
                if cash_sell_rate <= 0:
                    cash_sell_rate = None

                if cash_buy_rate <= 0:
                    cash_buy_rate = None

                if is_float_ok(cash_sell_rate) or is_float_ok(cash_buy_rate):
                     cash_exchange_rate = ExchangeRate(currency.code, convert_to_float(cash_buy_rate),
                                                  convert_to_float(cash_sell_rate))
                     exchange_dict[CASH] = cash_exchange_rate

            if transfer_rate is not None:
                transfer_rate_float = convert_to_float(transfer_rate)

                if (transfer_rate_float > 0):
                    is_original_rate = True

                    if currency.code == Currency.USD.code and transfer_rate_float > 3:
                        transfer_rate_float = convert_to_reverse_float(transfer_rate)
                        is_original_rate = False

                    exchange_rate = ExchangeRate(currency.code, rate=transfer_rate_float)
                    if is_original_rate == False:
                        exchange_rate.set_original_rate(convert_to_float(transfer_rate))

                    exchange_dict[TRANSFER] = exchange_rate

    return exchange_dict


def get_rates_from_multinet_trust() -> List[CompanyExchangeRates] | None:
    content = make_get_request_with_proxy(ExchangeBusinessExchangeUrl.MULTINET_TRUST_EXCHANGE)
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

                # update_date = extract_update_date(soup)

                # if update_date is not None:
                #    cash_exchange_rates.set_scrape_date(update_date)
                #    transfer_exchange_rates.set_scrape_date(update_date)

    cash_exchange_rates = CompanyExchangeRates(cash_exchange_rates)
    cash_exchange_rates.set_exchange_type(ExchangeType.CASH)
    cash_exchange_rates.set_current_scrape_date()

    transfer_exchange_rates = CompanyExchangeRates(transfer_exchange_rates)
    transfer_exchange_rates.set_exchange_type(ExchangeType.TRANSFER)
    transfer_exchange_rates.set_current_scrape_date()

    exchange_rates = []
    exchange_rates.append(cash_exchange_rates)
    exchange_rates.append(transfer_exchange_rates)
    #  exchange_rates.append(transfer_exchange_rates) TODO need to fix tranfer rates
    return exchange_rates


def scrape_multinet_trust() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_multinet_trust()
        if (company_exchange_rates is None):
            return None
        exchange_company = ExchangeCompany(ExchangeBusinessNames.MULTINET_TRUST_EXCHANGE,
                                           ExchangeBusinessUrl.MULTINET_TRUST_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)

        exchange_company.set_exchange_rates(company_exchange_rates)

        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping ', ExchangeBusinessNames.MULTINET_TRUST_EXCHANGE, err)
    return None
