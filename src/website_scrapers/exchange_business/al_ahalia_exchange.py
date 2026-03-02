from src.util.common_classes.company_data import ExchangeBusinessNames, ExchangeBusinessUrl, ExchangeBusinessApiUrl, \
    ExchangeBusinessExchangeUrl
from src.util.common_classes.exchange_company import ExchangeCompany, ExchangeCompanyType, CompanyExchangeRates, \
    ExchangeRate, Currency, ExchangeType
from src.util.scraping_util.request_util import make_get_request_with_proxy, make_get_request_with_parsed_html
from src.util.tool.json_util import parse_string_to_json
from src.util.tool.string_util import find_substring_index, convert_to_float


def get_rates_from_al_ahali() -> CompanyExchangeRates | None:
    html = make_get_request_with_parsed_html(ExchangeBusinessExchangeUrl.AL_AHALIA_EXCHANGE)
    transfer_rates = []

    if html is not None:
        # json_scripts = html.find_all('script')
        json_scripts = html.find_all('script', id="cc-inline-js-extra")
        if json_scripts is not None:
            for json_script in json_scripts:
                json_script = json_script.string.strip()
                start_index = find_substring_index(json_script, "{")
                end_index = find_substring_index(json_script, "}")

                if start_index > -1 and end_index > -1 and end_index > start_index:
                    json_content = parse_string_to_json(json_script[start_index:end_index + 1])
                    json_keys = json_content.keys()
                    for key in json_keys:
                        if (key != 'ajax_url'):
                            value = json_content[key]
                            if (key == 'phpr'):
                                key = 'php'
                            key = key.upper()
                            currency = Currency.get_currency(key)
                            rate = convert_to_float(value)
                            if currency is not None and rate > 0:
                                transfer_rate = ExchangeRate(currency, rate=rate)
                                transfer_rates.append(transfer_rate)

    company_exchange_rates = CompanyExchangeRates(transfer_rates)
    company_exchange_rates.set_current_scrape_date()
    company_exchange_rates.set_exchange_type(ExchangeType.TRANSFER)
    return company_exchange_rates


def scrape_al_ahalia_exchange() -> ExchangeCompany | None:
    try:
        company_exchange_rates = get_rates_from_al_ahali()
        exchange_company = ExchangeCompany(ExchangeBusinessNames.AL_AHALIA_EXCHANGE,
                                           ExchangeBusinessUrl.AL_AHALIA_EXCHANGE,
                                           ExchangeCompanyType.EXCHANGE_BUSINESS)

        exchange_company.add_exchange_rate(company_exchange_rates)

        return exchange_company
    except Exception as err:
        # TODO log this
        print('Error while scraping ', ExchangeBusinessNames.AL_AHALIA_EXCHANGE, err)
    return None
