from typing import List

from bs4 import BeautifulSoup, PageElement

from src.util.common_classes.company_data import BankName, BankUrl, BankExchangeRateUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, Currency, ExchangeRate, \
    CompanyExchangeRates, ExchangeType
from src.util.scraping_util.request_util import make_get_request_with_proxy
from src.util.tool.string_util import convert_to_float


def get_currency_from_element(currency_element: PageElement | None) -> Currency | None:
    if currency_element is not None:
        parents = currency_element.parent()
        if (parents is not None and len(parents) > 0):
            for parent in parents:
                currency_code = parent.getText()
                if currency_code is not None and Currency.get_currency(currency_code.strip()) is not None:
                    return Currency.get_currency(currency_code.strip())
    return None


def get_rates_from_ajman_bank() -> List[CompanyExchangeRates]:
    content = make_get_request_with_proxy(BankExchangeRateUrl.AJMAN_BANK)
    cash_exchange_rates = []
    transfer_exchange_rates = []

    if (content != None):
        soup = BeautifulSoup(content, 'html.parser')
        list_elements = soup.select('.list-group.bulk_data_list > .list-group-item > .row')

        if list_elements and len(list_elements) > 0:
            for list_element in list_elements:

                currency = get_currency_from_element(list_element.find(class_='currency'))
                if currency is not None:
                    div_children = list_element.find_all("div", recursive=False)
                    for div_child in div_children:

                        class_values = div_child.get('class')

                        if 'mob_currency' not in class_values:
                            transaction_type_element = div_child.find(class_='primeVal')
                            if (transaction_type_element is not None):
                                transaction_type = transaction_type_element.get_text()
                                buy_sell_elements = div_child.find_all('p')
                                buy_value = None
                                sell_value = None

                                if (buy_sell_elements is not None):
                                    for element in buy_sell_elements:
                                        element_text = element.get_text()
                                        element_text = element_text.replace('\t', '').replace('\n', '')
                                        if 'Sell' in element_text:
                                            sell_value = element_text.replace('Sell :', '').strip()

                                        elif 'Buy' in element_text:
                                            buy_value = element_text.replace('Buy :', '').strip()
                                exchange_rate = ExchangeRate(currency.code, convert_to_float(buy_value),
                                                             convert_to_float(sell_value))
                                if transaction_type == 'Cash':
                                    cash_exchange_rates.append(exchange_rate)
                                elif transaction_type == 'Transfer':
                                    transfer_exchange_rates.append(exchange_rate)

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


def scrape_ajman_bank() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_ajman_bank()
        # company_exchange_rates = parse_rates(raw_rates)
        exchange_company = ExchangeCompany(BankName.AJMAN_BANK,
                                           BankUrl.AJMAN_BANK,
                                           ExchangeCompanyType.NATIONAL_BANK)
        exchange_company.set_exchange_rates(company_exchange_rates)
        # exchange_company.set_exchange_rates(company_exchange_rates)
        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping ajman bank data', err)
    return None


