import time

from bs4 import BeautifulSoup

from src.util.common_classes.company_data import ExchangeBusinessNames, ExchangeBusinessUrl, ExchangeBusinessExchangeUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, CompanyExchangeRates, \
    ExchangeRate, Currency, ExchangeType
from src.util.tool.json_util import parse_string_to_json, get_value_from_json
from src.util.tool.proxy import get_random_proxy_for_request
from src.util.tool.string_util import convert_to_float
import requests
import ssl

from requests.adapters import HTTPAdapter

# INR , GBP , EUR ,CAD , LKR ,PKR , PHP ,EGP ,BDT
class TLSAdapter(HTTPAdapter):

    def _get_ssl_context(self):
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        return ctx

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self._get_ssl_context()
        return super().init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        kwargs['ssl_context'] = self._get_ssl_context()
        return super().proxy_manager_for(*args, **kwargs)


def get_session_with_proxy(url):
    session = requests.Session()

    # Allow weak SSL
    session.mount("https://", TLSAdapter())

    # Set proxy
    session.proxies = get_random_proxy_for_request()
    session.headers = {
        'user-agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
        'referer':'https://alrostamaniexchange.com'
    }
    response = session.get(url, timeout=10)
    return response.content


def get_currency_list():
    content = get_session_with_proxy(ExchangeBusinessExchangeUrl.AL_ROSTAMANI_EXCHANGE)

    html = BeautifulSoup(content, 'html.parser')
    # html = make_get_request_with_parsed_html(ExchangeBusinessExchangeUrl.AL_ROSTAMANI_EXCHANGE,verify=False)
    currencies = set()

    if html is not None:
        currency_list_element = html.select(".currency-list .currency-options img")
        for currency_element in currency_list_element:
            currency = currency_element.get('data-currency')
            if currency is not None:
                currencies.add(currency)
        return currencies
    return None

def request_json_document(url:str,count=0):
    # json_data_string = make_get_request_with_proxy(url)
    json_data_string = get_session_with_proxy(url)
    json_data = parse_string_to_json(json_data_string)
    if json_data is None and count < 3:
        count = count +1
        time.sleep(2)
        return request_json_document(url,count)
    return json_data

def scrape_al_rostamani_exchange_rates() -> CompanyExchangeRates | None:
    transfer_rates = []
    #currency_list = get_currency_list()
    currency_list = ['INR' ,'GBP' , 'EUR' ,'CAD' , 'LKR' ,'PKR' , 'PHP' ,'EGP' ,'BDT']
    if currency_list is not None:
        for currency_code in currency_list:
            url = "https://xe.alrostamaniexchange.com/rateenquiry?ForeignCurrency=" + currency_code + "&LCAmount=10&FCAmount=0.00"
            # json_data_string = make_get_request_with_proxy(url)
            json_data = request_json_document(url)

            if json_data is not None:
                rate = get_value_from_json(json_data, 'DivisionalRate')
                if rate is not None:
                    rate_float = convert_to_float(rate)
                    currency = Currency.get_currency(currency_code)
                    if currency is not None:
                        exchange_rate = ExchangeRate(currency.code, rate=rate_float)
                        transfer_rates.append(exchange_rate)

    company_exchange_rates = CompanyExchangeRates(transfer_rates)
    company_exchange_rates.set_exchange_type(ExchangeType.TRANSFER)
    company_exchange_rates.set_current_scrape_date()
    return company_exchange_rates


def scrape_al_rostamani_exchange_exchange() -> ExchangeCompany | None:
   try:
     company_exchange_rates = scrape_al_rostamani_exchange_rates()

     if company_exchange_rates is None:
         return None

     exchange_company = ExchangeCompany(ExchangeBusinessNames.AL_ROSTAMANI_EXCHANGE,
                                       ExchangeBusinessUrl.AL_ROSTAMANI_EXCHANGE,
                                       ExchangeCompanyType.EXCHANGE_BUSINESS)
     exchange_company.add_exchange_rate(company_exchange_rates)
     return exchange_company
   except Exception as err:
       print('Error while scraping ', ExchangeBusinessNames.AL_ROSTAMANI_EXCHANGE, err)
   return None


scrape_al_rostamani_exchange_exchange()