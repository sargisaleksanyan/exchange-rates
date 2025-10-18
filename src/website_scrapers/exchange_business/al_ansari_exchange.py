import random
import time

from bs4 import BeautifulSoup

from src.util.common_classes.company_data import ExchangeBusinessNames, ExchangeBusinessExchangeUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, ExchangeRate, Currency, \
    CompanyExchangeRates
from src.util.scraping_util.request_util import make_get_request_with_proxy, make_post_request_with_proxy
from src.util.tool.json_util import parse_string_to_json, get_value_from_json
from src.util.tool.string_util import convert_to_float

security_key = '7be9f96be0'
currency_request_url = 'https://alansariexchange.com/wp-admin/admin-ajax.php'
SECUREITY_JSON_HEADER_NAME = 'ajax_nonce'
CURRENCY_URL_HEADER_NAME = 'ajax_url'
CURRENCY_HEADER_NAME = 'data-ccyname'
CURRENCY_DATA_CNTCODE = 'data-cntcode'
CURRENCY_TO_HEADER_NAME = 'data-toccy'


class CurrencyRequestData:
    def __init__(self, currency_from, currency_to='91', transaction_type='S'):
        # self.currency_code = currency_code
        self.currency_from = currency_from
        self.currency_to = currency_to
        self.transaction_type = transaction_type


class ApiRequestParameters:
    def __init__(self, url: str, security_key: str):
        self.url = url
        self.security_key = security_key


def sleep_random_time():
    sleep_time = random.randint(1100, 2100) / 1000
    time.sleep(sleep_time)


def get_currency_buy_rate(currency_data: CurrencyRequestData):
    return None


def extract_api_request_parameters(html: BeautifulSoup) -> ApiRequestParameters | None:
    json_scripts = html.find_all('script', id="ajax-script-js-extra")

    for json_script in json_scripts:
        json_content = json_script.string.strip()
        if SECUREITY_JSON_HEADER_NAME in json_content:
            first_index = json_content.find("{")
            last_index = json_content.find("}")
            if first_index > -1 and last_index > -1 and last_index > first_index:
                sub_string = json_content[first_index:last_index + 1]
                json = parse_string_to_json(sub_string)
                if json is not None:
                    security_key = get_value_from_json(json, SECUREITY_JSON_HEADER_NAME)
                    currency_request_url = get_value_from_json(json, CURRENCY_URL_HEADER_NAME)
                    if security_key is not None and currency_request_url is not None:
                        return ApiRequestParameters(currency_request_url, security_key)

    return None


def extract_aed_currency_data(html: BeautifulSoup):
    uae_currency_element = html.find(class_='united_arab_emirates')
    if uae_currency_element is None:
        uae_currency_element = html.find(class_='send-currency-name')
    if uae_currency_element is not None:
        result = uae_currency_element.get(CURRENCY_DATA_CNTCODE)
        return result
    return None


def get_currency_rate(currency_request_data: CurrencyRequestData,
                      api_request_parameters: ApiRequestParameters) -> float | None:
    sleep_random_time()

    body = {
        "action": "foreign_action",
        "currfrom": currency_request_data.currency_from,
        "currto": currency_request_data.currency_to,
        "cntcode": currency_request_data.currency_from,
        "amt": "1",
        "security": api_request_parameters.security_key,
        "trtype": currency_request_data.transaction_type
    }
    result = make_post_request_with_proxy(api_request_parameters.url, body, is_url_encoded=True)
    if result is not None:
        json_result = parse_string_to_json(result)
        return convert_to_float(get_value_from_json(json_result, 'rate'))

    return None


def get_rates_from_al_ansari():
    content = make_get_request_with_proxy(ExchangeBusinessExchangeUrl.AL_ANSARI_EXCHANGE)

    if content is not None:
        soup = BeautifulSoup(content, 'html.parser')
        currency_wrapper = soup.find(class_='currency-select')

        if currency_wrapper is not None:
            passed_currency_codes = set()

            currency_element_list = currency_wrapper.find_all('li')
            if currency_element_list is None or len(currency_element_list) == 0:
                return None
            request_parameters = extract_api_request_parameters(soup)
            aed_to_code = extract_aed_currency_data(soup)

            if request_parameters is None or aed_to_code is None:
                return None

            exchange_rates = []

            for currency_element in currency_element_list:
                currency_span = currency_element.find('span')
                if currency_span is None:
                    continue
                currency_name = currency_span.get(CURRENCY_HEADER_NAME)

                if currency_name not in passed_currency_codes and Currency.get_currency(currency_name) is not None:
                    currency_code_number = currency_span.get(CURRENCY_DATA_CNTCODE)
                    request_sell_data = CurrencyRequestData(
                        currency_from=currency_code_number,
                        currency_to=aed_to_code, transaction_type='S')
                    request_buy_data = CurrencyRequestData(
                        currency_from=currency_code_number,
                        currency_to=aed_to_code, transaction_type='B')
                    sell_rate = get_currency_rate(request_sell_data, request_parameters)
                    if sell_rate is None:
                        continue

                    buy_rate = get_currency_rate(request_buy_data, request_parameters)
                    if buy_rate is None or sell_rate > buy_rate:
                        continue
                    passed_currency_codes.add(currency_name)
                    exchange_rate = ExchangeRate(Currency.get_currency(currency_name).code, sell_rate=sell_rate,
                                                 buy_rate=buy_rate)
                    exchange_rates.append(exchange_rate)

            company_exchange_rates = CompanyExchangeRates(exchange_rates)
            company_exchange_rates.set_current_scrape_date()
            return company_exchange_rates
    return None


def scrape_al_ansari_exchange() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_al_ansari()
        # company_exchange_rates = parse_rates
        if company_exchange_rates is None:
            return None;
        exchange_company = ExchangeCompany(ExchangeBusinessNames.AL_ANSARI_EXCHANGE,
                                           ExchangeBusinessExchangeUrl.JOYALUKKAS_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)
        exchange_company.add_exchange_rate(company_exchange_rates)
        # exchange_company.set_exchange_rates(company_exchange_rates)
        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping emirates islamic bank data', err)
    return None


scrape_al_ansari_exchange()
