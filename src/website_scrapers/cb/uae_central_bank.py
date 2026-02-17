import re
from datetime import datetime

from bs4 import BeautifulSoup

from src.util.common_classes.company_data import BankName, BankUrl, BankExchangeRateUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, CompanyExchangeRates, \
    ExchangeRate, get_currency_code_by_name
from src.util.scraping_util.browser_util import get_website_content_by_browser

CURRENCY_HEADER = 'currency'
RATES_HEADER = 'rates'


def get_table_headers(table_header_tr):
    if table_header_tr is None:
        return None

    ths = table_header_tr.find_all('th')
    headers = {

    }

    for i in range(0, len(ths)):
        th = ths[i]
        header_text = th.get_text()

        if header_text is not None:
            header_text = header_text.strip().lower()
            if header_text == CURRENCY_HEADER or header_text == RATES_HEADER:
                headers[header_text] = i
    return headers


def extract_update_date(html: BeautifulSoup):
    updated_at_element = html.find("p", string=re.compile(r"Last updated:"))
    if (updated_at_element is not None):
        try:
            updated_at_text = updated_at_element.get_text().strip()
            updated_at_text = updated_at_text.replace("Last updated:", "").replace("\n", "")

            dt = datetime.strptime(
                updated_at_text,
                "%A %d %B %Y %I:%M:%S %p"
            )
            return dt
        except Exception as err:
            print('Error occured while parsing string ', BankName.CENTRAL_BANK, err)

    return None


def get_rates_from_html(html: BeautifulSoup):
    tables = html.find_all('table')

    exchange_rates = []

    for table in tables:
        table_header_tr = table.select_one('thead > tr')
        table_data_rows = table.select('tbody > tr')

        header_indices = get_table_headers(table_header_tr)

        if header_indices is not None and CURRENCY_HEADER in header_indices and RATES_HEADER in header_indices and table_data_rows is not None:

            currency_index = header_indices[CURRENCY_HEADER]
            rate_index = header_indices[RATES_HEADER]

            for table_data_row in table_data_rows:
                row_tds = table_data_row.find_all('td')

                if row_tds is not None and len(row_tds) >= currency_index and len(row_tds) >= rate_index:
                    currency_name = row_tds[currency_index].get_text().strip()
                    rate = row_tds[rate_index].get_text().strip()

                    # if currency_name is not None and rate is not None and currency_name not in currency_name_to_code:
                    if currency_name is not None and rate is not None:
                        try:
                            currency_code = get_currency_code_by_name(currency_name)
                            if currency_code is not None:
                                exchange_rate = ExchangeRate(currency=currency_code, rate=rate)
                                exchange_rates.append(exchange_rate)
                        except Exception as err:
                            print('Exception', err)
    return exchange_rates


def get_rates_from_central_bank() -> CompanyExchangeRates | None:

    content = get_website_content_by_browser(BankExchangeRateUrl.CENTRAL_BANK)
    if content is not None:
        soup = BeautifulSoup(content, 'html.parser')
        rates = get_rates_from_html(soup)
        central_bank_rate = CompanyExchangeRates(rates)
        central_bank_rate.set_current_scrape_date()
        central_bank_rate.set_update_date(extract_update_date(soup))
        return central_bank_rate
        # central_bank_rate.set_update_date()
    return None


def scrape_central_bank() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_central_bank()
        # company_exchange_rates = parse_rates(raw_rates)
        exchange_company = ExchangeCompany(BankName.CENTRAL_BANK,
                                           BankUrl.CENTRAL_BANK,
                                           ExchangeCompanyType.CENTRAL_BANK)
        exchange_company.add_exchange_rate(company_exchange_rates)

        # exchange_company.set_exchange_rates(company_exchange_rates)
        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping emirates central bank data', err)

