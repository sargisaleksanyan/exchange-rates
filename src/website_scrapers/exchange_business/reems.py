from bs4 import BeautifulSoup, PageElement
from src.util.common_classes.company_data import ExchangeBusinessNames, \
    ExchangeBusinessUrl, ExchangeBusinessExchangeUrl
from src.util.common_classes.exchange_company import ExchangeCompany, CompanyExchangeRates, \
    ExchangeCompanyType, Currency, ExchangeRate
from src.util.scraping_util.request_util import make_get_request_with_proxy
from src.util.tool.string_util import convert_to_float

CURRENCY_HEAD = 'Currency'
BUY_RATE_HEAD = 'Buy'
SELL_RATE_HEAD = 'Sell'

currency_data = {
    'Australian Dollor': 'AUD',
    'Swiss Franc': 'CHF',
    'Singapore Dollar': 'SGD',
    'Phillipines Peso': 'PHP',
    'US Dollar': 'USD',
    'Euro': 'EUR',
    'UK Pound': 'GBP',
    'Canadian Dollar': 'CAD',
    'New Zealand DOLLAR': 'NZD',
    'Japanese Yen': 'JPY',
    'Swedish Krona': 'SEK',
    'Norwegian Krone': 'NOK',
    'Danish Krone': 'DKK',
    'Labenese Pound': 'LBP',
    'Egypt Pound': 'EGP',
    'Turkey Lira': 'TRY',
    'Jordan Dinar': 'JOD',
    'Saudi Riyal': 'SAR',
    'Bahrain Dinar': 'BHD',
    'Oman Rial': 'OMR',
    'Yemen Riyal': 'YER',
    'Scotland Pound': 'SCO',  # Not official, using 'SCO' as placeholder
    'S. Africa': 'ZAR',
    'Tunis Dinar': 'TND',
    'Ethiopian Birr': 'ETB',
    'Kuwait Dinar': 'KWD',
    'Algerian Dinar': 'DZD',
    'Morocco Dirham': 'MAD',
    'Indonesian Rupiah': 'IDR',
    'Mauritius Rupee': 'MUR',
    'Thailand Bhat': 'THB',
    'Chinese Yuan': 'CNY',
    'Taiwan Dollar': 'TWD',
    'Brunei Dollar': 'BND',
    'Malaysian Ringgit': 'MYR',
    'Indian Ruppee': 'INR'
}


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


def get_currency(td_elements, index: int) -> Currency | None:
    currency_name = get_element_text(td_elements, index)
    if currency_name in currency_data:
        currency_code = currency_data[currency_name]
        return Currency.get_currency(currency_code)
    else:
        print(currency_name, ' has not been found')
    return None


def get_element_text(td_elements, index: int):
    if (td_elements is not None and len(td_elements) > index):
        element = td_elements[index]
        if (element is not None):
            value = element.get_text().strip()
            return value

    return None


def extract_reems_exchange_rates() -> CompanyExchangeRates | None:
    content = make_get_request_with_proxy(ExchangeBusinessExchangeUrl.REEMS_EXCHANGE)

    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find(class_='table')
    table_headers = get_table_headers(table)

    if (table is None):
        return None

    table_rows = table.find_all('tr')

    if table_rows is None or len(table_rows) == 0:
        return None

    exchange_rates = []

    for table_row in table_rows:
        table_data_elements = table_row.find_all('td')
        if table_data_elements is not None and len(table_data_elements) > 0:
            currency = get_currency(table_data_elements, table_headers[CURRENCY_HEAD])
            buy_rate = get_element_text(table_data_elements, table_headers[BUY_RATE_HEAD])
            sell_rate = get_element_text(table_data_elements, table_headers[SELL_RATE_HEAD])

            if currency is not None and buy_rate is not None and sell_rate is not None:
                buy = convert_to_float(buy_rate)
                sell = convert_to_float(sell_rate)

                if buy > 0 and sell > 0 and sell > buy:
                    exchange_rate = ExchangeRate(currency.code, buy, sell)
                    exchange_rates.append(exchange_rate)

    company_exchange_rates = CompanyExchangeRates(exchange_rates)
    company_exchange_rates.set_current_scrape_date()

    return company_exchange_rates


def scrape_reems_exchange() -> ExchangeCompany | None:
    try:
        company_exchange_rates = extract_reems_exchange_rates()
        exchange_company = ExchangeCompany(ExchangeBusinessNames.REEMS_EXCHANGE, ExchangeBusinessUrl.REEMS_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)
        exchange_company.add_exchange_rate(company_exchange_rates)
        return exchange_company

    except Exception as err:
        print('Error occurred while scraping ', ExchangeBusinessNames.REEMS_EXCHANGE, err)
    return None
