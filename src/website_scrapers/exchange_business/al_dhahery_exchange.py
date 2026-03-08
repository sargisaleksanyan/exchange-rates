
from bs4 import PageElement

from src.util.common_classes.company_data import ExchangeBusinessNames, ExchangeBusinessExchangeUrl, \
    ExchangeBusinessApiUrl, ExchangeBusinessUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, ExchangeRate, Currency, \
    CompanyExchangeRates, ExchangeType
from src.util.scraping_util.request_util import make_get_request_with_parsed_html
from src.util.tool.string_util import convert_to_float, get_element_text

CURRENCY = 'Code'
CASH_BUY_RATE = 'Buy'
CASH_SELL_RATE = 'Sell'


def get_table_headers(page_element: PageElement) -> dict:
    element_index_dict = {

    }

    table_headers = page_element.find_all('th')
    if (table_headers is None):
        return element_index_dict

    for i in range(0, len(table_headers)):
        th = table_headers[i]
        if th is not None and th.get_text() is not None:
            th_text = th.get_text().strip().lower()

            if (CURRENCY.lower() in th_text):
                element_index_dict[CURRENCY] = i

            elif (CASH_BUY_RATE.lower() in th_text):
                element_index_dict[CASH_BUY_RATE] = i

            elif (CASH_SELL_RATE.lower() in th_text):
                element_index_dict[CASH_SELL_RATE] = i

    return element_index_dict


def extract_exchange_from_row_element(table_row: PageElement, table_headers: dict) -> ExchangeRate | None:
    if (table_row is None):
        return

    table_data_list = table_row.find_all('td')

    if (table_data_list is not None):
        currency_code = get_element_text(table_data_list, table_headers, CURRENCY)
        currency = Currency.get_currency(currency_code)

        if (currency is not None):
            cash_buy_rate = get_element_text(table_data_list, table_headers, CASH_BUY_RATE)
            cash_sell_rate = get_element_text(table_data_list, table_headers, CASH_SELL_RATE)

            if cash_buy_rate is not None and cash_sell_rate is not None:
                cash_buy_rate = convert_to_float(cash_buy_rate)
                cash_sell_rate = convert_to_float(cash_sell_rate)
                if cash_sell_rate <= 0:
                    cash_sell_rate = None

                if cash_buy_rate <= 0:
                    cash_buy_rate = None

                cash_exchange_rate = ExchangeRate(currency.code, convert_to_float(cash_buy_rate),
                                                  convert_to_float(cash_sell_rate))
                return cash_exchange_rate
    return None


def get_rates_from_al_dhahery() -> CompanyExchangeRates | None:
    headers = {
        'referer': ExchangeBusinessExchangeUrl.AL_DHAHERY_EXCHANGE
    }

    html_page = make_get_request_with_parsed_html(ExchangeBusinessApiUrl.AL_DHAHERY_EXCHANGE,
                                                  given_headers=headers)
    if (html_page is None):
        return None

    table = html_page.find('table')

    if table is None:
        return None
    headers = get_table_headers(table)

    if headers is None:
        return None

    cash_exchange_rates = []

    trs = table.find_all('tr')
    if (trs is not None):
        for tr in trs:
            exchange_rate = extract_exchange_from_row_element(tr, headers)
            cash_exchange_rates.append(exchange_rate)

    cash_exchange_rates = CompanyExchangeRates(cash_exchange_rates)
    cash_exchange_rates.set_exchange_type(ExchangeType.CASH)
    cash_exchange_rates.set_current_scrape_date()
    return cash_exchange_rates


def scrape_al_dhahery_exchange() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_al_dhahery()
        if (company_exchange_rates is None):
            return None
        exchange_company = ExchangeCompany(ExchangeBusinessNames.AL_DHAHERY_EXCHANGE,
                                           ExchangeBusinessUrl.AL_DHAHERY_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)

        exchange_company.add_exchange_rate(company_exchange_rates)

        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping ', ExchangeBusinessNames.MESRKANLOO_INTERNATIONAL_EXCHANGE, err)
    return None
