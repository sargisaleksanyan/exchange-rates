#
from datetime import datetime

from src.util.common_classes.company_data import ExchangeBusinessNames, ExchangeBusinessUrl, ExchangeBusinessExchangeUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, CompanyExchangeRates, \
    Currency, ExchangeRate, ExchangeType
from src.util.scraping_util.request_util import make_get_request_with_parsed_html
from src.util.tool.string_util import convert_to_float


def extract_update_date(update_date_text):
    if update_date_text is not None:
        try:
            update_date_text = update_date_text.replace("\r", "").replace("\n", "").replace("\r\n", "").strip()
            dt = datetime.strptime(update_date_text, "%d/%m/%Y %H:%M")
            return dt
        except Exception as err:
            print('Error occurred while converting date for ', ExchangeBusinessNames.LARI_EXCHANGE, err)
    return None


def scrape_lari_exchange_rates() -> CompanyExchangeRates | None:
    html = make_get_request_with_parsed_html(ExchangeBusinessExchangeUrl.LARI_EXCHANGE, verify=False)
    if (html is None):
        return None
    currency_rate_elements = html.select(".item-wrap .item")

    transfer_rates = []

    last_updated = None
    if currency_rate_elements is not None:
        for currency_rate_element in currency_rate_elements:
            table_rows = currency_rate_element.find('tr')
            if table_rows is None:
                continue
            row_text = table_rows.getText()
            if row_text is None:
                continue

            trs = currency_rate_element.select('tr')
            if trs is None or len(trs) == 0:
                continue

            last_element = trs[len(trs) - 1]
            tds = last_element.select('td')

            if len(tds) == 0:
                continue

            if 'LAST UPDATED' in row_text:
                last_updated_text = tds[0].getText()
                last_updated = extract_update_date(last_updated_text)
            else:
                if tds is not None and len(tds) == 2:
                    currency_text = tds[0].getText()
                    rate_text = tds[1].getText()

                    if (currency_text is not None and rate_text is not None):
                        currency = Currency.get_currency(currency_text.strip())
                        if currency is None:
                            continue
                        rate = convert_to_float(rate_text.strip())
                        if rate is not None:
                            transfer_rate = ExchangeRate(currency.code, rate=rate)
                            transfer_rates.append(transfer_rate)

    company_exchange_rates = CompanyExchangeRates(transfer_rates)
    company_exchange_rates.set_current_scrape_date()
    if last_updated is not None:
        company_exchange_rates.set_update_date(last_updated)
    company_exchange_rates.set_exchange_type(ExchangeType.TRANSFER)
    return company_exchange_rates


def scrape_lari_exchange() -> ExchangeCompany | None:
    try:
        company_exchange_rates = scrape_lari_exchange_rates()

        if company_exchange_rates is None:
            return None

        exchange_company = ExchangeCompany(ExchangeBusinessNames.LARI_EXCHANGE,
                                           ExchangeBusinessUrl.LARI_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)
        exchange_company.add_exchange_rate(company_exchange_rates)
        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping ', ExchangeBusinessNames.LARI_EXCHANGE, err)
    return None


