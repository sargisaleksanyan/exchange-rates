import random
import time

from bs4 import BeautifulSoup

from src.util.common_classes.company_data import ExchangeBusinessNames, ExchangeBusinessExchangeUrl, ExchangeBusinessUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, ExchangeRate, Currency, \
    CompanyExchangeRates, ExchangeType, create_exchange_rate
from src.util.scraping_util.request_util import make_get_request_with_proxy, make_post_request_with_proxy
from src.util.tool.json_util import parse_string_to_json, get_value_from_json
from src.util.tool.string_util import convert_to_float, convert_to_reverse_float, is_float_ok

security_key = '7be9f96be0'
currency_request_url = 'https://alansariexchange.com/wp-admin/admin-ajax.php'
SECUREITY_JSON_HEADER_NAME = 'ajax_nonce'
CURRENCY_URL_HEADER_NAME = 'ajax_url'
CURRENCY_HEADER_NAME = 'data-ccyname'
CURRENCY_DATA_CNTCODE = 'data-cntcode'
CURRENCY_TO_HEADER_NAME = 'data-toccy'
TRANSFER_TYPE = 'BT'
TRANSFER_ACTION_TYPE = 'convert_action'
FOREIGN_ACTION_TYPE = 'foreign_action'


class CurrencyRequestData:
    def __init__(self, currency_from, currency_to='91', transaction_type='S'):
        # self.currency_code = currency_code
        self.currency_from = currency_from
        self.currency_to = currency_to
        self.transaction_type = transaction_type
        self.action_type = FOREIGN_ACTION_TYPE

    def set_action_type(self, action_type=FOREIGN_ACTION_TYPE):
        self.action_type = action_type


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


def get_currency_rate_text(currency_request_data: CurrencyRequestData,
                           api_request_parameters: ApiRequestParameters) -> str | None:
    sleep_random_time()

    body = {
        "action": currency_request_data.action_type,
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
        rate = get_value_from_json(json_result, 'rate')

        if rate is None:
            rate = get_value_from_json(json_result, 'get_rate')
        return rate

    return None


def get_currency_rate(currency_request_data: CurrencyRequestData,
                      api_request_parameters: ApiRequestParameters) -> float | None:
    currency_rate_text = get_currency_rate_text(currency_request_data, api_request_parameters)
    if (currency_rate_text is None):
        return None
    return convert_to_float(currency_rate_text)


def get_sell_and_buy_rate(currency_name, currency_code_number, aed_to_code, request_parameters):
    request_sell_data = CurrencyRequestData(
        currency_from=currency_code_number,
        currency_to=aed_to_code, transaction_type='S')

    request_buy_data = CurrencyRequestData(
        currency_from=currency_code_number,
        currency_to=aed_to_code, transaction_type='B')
    sell_rate = get_currency_rate(request_sell_data, request_parameters)

    buy_rate = get_currency_rate(request_buy_data, request_parameters)

    if is_float_ok(buy_rate) or is_float_ok(sell_rate):
       exchange_rate =  create_exchange_rate (Currency.get_currency(currency_name).code, sell_rate=buy_rate,
                                 buy_rate=sell_rate)
       return exchange_rate
    return None


def get_transfer_rate(currency_name, currency_code_number, aed_to_code, request_parameters):
    request_transfer_data = CurrencyRequestData(
        currency_from=currency_code_number,
        currency_to=aed_to_code, transaction_type=TRANSFER_TYPE)

    request_transfer_data.set_action_type(TRANSFER_ACTION_TYPE)

    transfer_rate_text = get_currency_rate_text(request_transfer_data, request_parameters)

    if transfer_rate_text is None:
        return None

    # reverse_rate = convert_to_reverse_float(transfer_rate_text)
    rate = convert_to_float(transfer_rate_text)
    exchange_rate = ExchangeRate(Currency.get_currency(currency_name).code, rate=rate)
    # exchange_rate.set_original_rate(convert_to_float(transfer_rate_text))
    return exchange_rate


def get_rates_from_al_ansari(url, is_cash_request=True):
    # content = make_get_request_with_proxy(ExchangeBusinessExchangeUrl.AL_ANSARI_EXCHANGE)
    content = make_get_request_with_proxy(url)

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
                    if (is_cash_request == True):
                        exchange_rate = get_sell_and_buy_rate(currency_name, currency_code_number, aed_to_code,
                                                              request_parameters)
                        if exchange_rate is not None:
                            exchange_rates.append(exchange_rate)
                    else:
                        exchange_rate = get_transfer_rate(currency_name, currency_code_number, aed_to_code,
                                                          request_parameters)
                        if exchange_rate is not None:
                            exchange_rates.append(exchange_rate)

                    passed_currency_codes.add(currency_name)

            company_exchange_rates = CompanyExchangeRates(exchange_rates)
            company_exchange_rates.set_current_scrape_date()
            return company_exchange_rates
    return None


def scrape_all_type_of_rates() -> list[CompanyExchangeRates]:

    cash_rates = get_rates_from_al_ansari(ExchangeBusinessExchangeUrl.AL_ANSARI_EXCHANGE)
    cash_rates.set_current_scrape_date()
    cash_rates.set_exchange_type(ExchangeType.CASH)

    transfer_rates = get_rates_from_al_ansari(ExchangeBusinessExchangeUrl.AL_ANSARI_EXCHANGE_TRANSFER_RATE_PAGE, False)
    transfer_rates.set_current_scrape_date()
    transfer_rates.set_exchange_type(ExchangeType.TRANSFER)


    return [cash_rates, transfer_rates]


def scrape_al_ansari_exchange() -> ExchangeCompany | None:
    try:
        company_exchange_rates = scrape_all_type_of_rates()

        if company_exchange_rates is None:
            return None

        exchange_company = ExchangeCompany(ExchangeBusinessNames.AL_ANSARI_EXCHANGE,
                                           ExchangeBusinessUrl.AL_ANSARI_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)
        exchange_company.set_exchange_rates(company_exchange_rates)
        # exchange_company.set_exchange_rates(company_exchange_rates)
        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping ', ExchangeBusinessNames.AL_ANSARI_EXCHANGE, err)
    return None
