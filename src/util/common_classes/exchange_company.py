from datetime import datetime,timezone
from enum import Enum
from typing import List
from zoneinfo import ZoneInfo

from src.util.common_classes.currency import currency_name_to_code
from src.util.tool.string_util import is_float_ok


UAE_TZ = ZoneInfo("Asia/Dubai")

def convert_to_utc_time(dt: datetime) -> datetime:
    try:
        if dt.tzinfo is None:
            # assign UAE timezone first
            dt = dt.replace(tzinfo=UAE_TZ)

        # convert to UTC
        return dt.astimezone(timezone.utc)

    except Exception as err:
        print('Error occurred while converting timezone', err)

    return dt


class Currency(Enum):
    AUD = ("AUD", "Australian Dollar")
    BHD = ("BHD", "Bahraini Dinar")
    BWP = ("BWP", "Botswana Pula")
    BYN = ("BYN", "Belarus Rouble")
    CAD = ("CAD", "Canadian Dollar")
    CYP = ("CYP", "Cyprus Pound")
    COP = ("COP", "Colombian Peso")
    CHF = ("CHF", "Swiss Franc")
    DKK = ("DKK", "Danish Kroner")
    EGP = ("EGP", "Egypt Pounds")
    EUR = ("EUR", "Euro")
    HKD = ("HKD", "Hong Kong Dollar")
    INR = ("INR", "Indian Rupee")
    JOD = ("JOD", "Jordanian Dinar")
    JPY = ("JPY", "Japanese Yen")
    KWD = ("KWD", "Kuwaiti Dinar")
    LKR = ("LKR", "Sri Lankan Rupee")
    MAD = ("MAD", "Moroccan Dirham")
    NOK = ("NOK", "Norwegian Kroner")
    NZD = ("NZD", "New Zealand Dollar")
    OMR = ("OMR", "Omani Riyal")
    PHP = ("PHP", "Philippine Peso")
    PKR = ("PKR", "Pakistan Rupee")
    SAR = ("SAR", "Saudi Riyal")
    SEK = ("SEK", "Swedish Kroner")
    SGD = ("SGD", "Singapore Dollar")
    THB = ("THB", "Thai Baht")
    USD = ("USD", "United States Dollar")
    ZAR = ("ZAR", "South Africa Rand")
    AMD = ("AMD", "Armenian Dram")
    ARS = ("ARS", "Argentine Peso")
    AZN = ("AZN", "Azerbaijani Manat")
    MVR = ("MVR", "Maldivian Rufiyaa")
    BDT = ("BDT", "Bangladeshi Taka")
    BRL = ("BRL", "Brazilian Real")
    KHR = ("KHR", "Cambodian Riel")
    CNH = ("CNH", "Chinese Yuan Renminbi")
    CNY = ("CNY", "Chinese Yuan Renminbi")
    ETB = ("ETB", "Ethiopian Birr")
    GEL = ("GEL", "Georgian Lari")
    IDR = ("IDR", "Indonesian Rupiah")
    IRR = ("IRR", "Iranian Rial")
    IQD = ("IQD", "Iraqi Dinar")
    ILS = ("ILS", "Israeli New Shekel")
    KZT = ("KZT", "Kazakhstani Tenge")
    KRW = ("KRW", "South Korean Won")
    LYD = ("LYD", "Libyan Dinar")
    MYR = ("MYR", "Malaysian Ringgit")
    MXN = ("MXN", "Mexican Peso")
    NGN = ("NGN", "Nigerian Naira")
    PLN = ("PLN", "Polish Złoty")
    QAR = ("QAR", "Qatari Riyal")
    RUB = ("RUB", "Russian Ruble")
    TRY = ("TRY", "Turkish Lira")
    UAH = ("UAH", "Ukrainian Hryvnia")
    UZS = ("UZS", "Uzbekistani Sum")
    AED = ("AED", "United Arab Emirates Dirham")
    UGX = ("UGX", "Ugandan Shilling")
    TTD = ("TTD", "Trin Tob Dollar")
    TND = ("TND", "Tunisian Dinar")
    TZS = ("TZS", "Tanzanian Shilling")
    TJS = ("TJS", "Tajikistani Somoni")
    TWD = ("TWD", "New Taiwan Dollar")
    SYP = ("SYP", "Syrian Pound")
    SDG = ("SDG", "Sudanese Pound")
    YER = ("YER", "Yemeni Rial")
    RSD = ("RSD", "Serbian Dinar")
    RWF = ("RWF", "Rwandan Franc")
    RON = ("RON", "Romanian Leu")
    NPR = ("NPR", "Nepalese Rupee")
    MMK = ("MMK", "Burmese Kyat")
    MNT = ("MNT", "Mongolian Tögrög")
    LBP = ('LBP', "Lebanese Pound")
    KGS = ('KGS', "Kyrgyz Som")
    KES = ('KES', "Kenyan Shilling")
    ISK = ('ISK', "Icelandic Króna")
    CLP = ('CLP', "Chilean Peso")
    AFA = ("AFN", "Afghan Afghani")
    ALL = ("ALL", "Albanian Lek")
    ANG = ("ANG", "Netherlands Antillean Guilder")
    AOA = ("AOA", "Angolan Kwanza")
    BGN = ("BGN", "Bulgarian Lev")
    BND = ("BND", "Brunei Dollar")
    BOB = ("BOB", "Bolivian Boliviano")
    BAM = ("BAM", "Bosnia and Herzegovina convertible mark")
    BSD = ("BSD", "Bahamian Dollar")
    CRC = ("CRC", "Costa Rican Colón")
    CUP = ("CUP", "Cuban Peso")
    CZK = ("CZK", "Czech Koruna")
    DZD = ("DZD", "Algerian Dinar")
    FJD = ("FJD", "Fijian Dollar")
    GHS = ("GHS", "Ghanaian Cedi")
    GTQ = ("GTQ", "Guatemalan Quetzal")
    HUF = ("HUF", "Hungarian Forint")
    KPW = ("KPW", "North Korean Won")
    LAK = ("LAK", "Lao Kip")
    MDL = ("MDL", "Moldovan Leu")
    MKD = ("MKD", "Macedonian Denar")
    MUR = ("MUR", "Mauritian Rupee")
    NAD = ("NAD", "Namibian Dollar")
    PEN = ("PEN", "Peruvian Sol")
    PYG = ("PYG", "Paraguayan Guarani")
    SRD = ("SRD", "Surinamese Dollar")
    VES = ("VES", "Venezuelan Bolívar Soberano")
    VND = ("VND", "Vietnamese Dong")
    XAG = ("XAG", "Silver Ounce")
    XAU = ("XAU", "Gold")
    XAF = ("XAF", "Central African CFA Franc")
    XCD = ("XCD", "East Caribbean Dollar")
    XOF = ("XOF", "West African CFA Franc")
    XPF = ("XPF", "CFP Franc")
    GBP = ("GBP", "British Pound Sterling")
    ZMW = ("ZMW", "Zambian Kwacha")
    TMT = ("TMT", "Turkmen manat")

    def __init__(self, code, fullname):
        self.code = code
        self.fullname = fullname

    def __str__(self):
        return f"{self.code} - {self.fullname}"

    def get_currency(currency):
        if (currency is None):
            return None
        currency = currency.strip()
        if isinstance(currency, Currency):
            return Currency[currency]
        if isinstance(currency, str) and currency in Currency._value2member_map_ or currency in (c.code for c in
                                                                                                 Currency):
            return Currency[currency]
        if currency.strip() != '':
            print('Currency has not been found', currency)  # TODO print this
        return None


def get_currency_code_by_name(currency_name):
    if currency_name is not None and currency_name.lower() in currency_name_to_code:
        currency_code = currency_name_to_code[currency_name.lower()]
        currency = Currency.get_currency(currency_code)

        if currency is not None:
            return currency.code
    if currency_name is not None and currency_name !='':
       print('Currency name has not been found ', currency_name)
    return None


class ExchangeCompanyType(Enum):
    CENTRAL_BANK = 'Central bank'
    NATIONAL_BANK = 'National bank'
    FOREIGN_BANK = 'Foreign bank'
    EXCHANGE_BUSINESS = 'Exchange business'


class ExchangeType(Enum):
    CASH = 'Cash'
    TRANSFER = 'Transfer'
    ONLINE = 'Online'



class ExchangeRate:
    def __init__(self, currency: str, buy_rate=None, sell_rate=None, rate=None):
        self.currency = currency
        self.buy = buy_rate
        self.sell = sell_rate
        self.rate = rate
        self.exchange_type = None
        self.update_date = None
        self.original_rate = None
        self.original_sell_rate = None
        self.original_buy_rate = None

    def set_exchange_type(self, exchange_type: ExchangeType):
        self.exchange_type = exchange_type

    def set_update_date(self, update_date):
        #update_date = convert_to_uae_time(update_date)
        update_date = convert_to_utc_time(update_date)

        self.update_date = update_date

    def set_original_rate(self, original_rate):
        self.original_rate = original_rate

    def set_original_buy_rate(self, original_buy_rate):
        self.original_buy_rate = original_buy_rate

    def set_original_sell_rate(self, original_sell_rate):
        self.original_sell_rate = original_sell_rate


class CompanyExchangeRates:
    def __init__(self, exchange_rates: List[ExchangeRate]):
        self.exchange_type = None
        self.update_date = None
        self.scrape_date = None
        self.exchange_rates = exchange_rates

    def add_exchange_rate(self, new_exchange_rate: ExchangeRate):
        if (self.exchange_rates == None):
            self.exchange_rates = []

        exists = False

        for exchange_rate in self.exchange_rates:
            if (new_exchange_rate.currency.code == exchange_rate.currency.code):
                exists = True

        if (exists == False):
            self.exchange_rates.append(new_exchange_rate)

    def set_exchange_type(self, exchange_type: ExchangeType):
        self.exchange_type = exchange_type

    def set_update_date(self, update_date):
        converted_date = convert_to_utc_time(update_date)
        self.update_date = converted_date


    def set_current_scrape_date(self):

        # uae_time = datetime.now(ZoneInfo("Asia/Dubai"))
        # utc_time = uae_time.astimezone(timezone.utc)
        self.scrape_date = datetime.now(timezone.utc)


class ExchangeCompany:
    def __init__(self, name: str, url: str, company_type: ExchangeCompanyType):
        self.name = name
        self.url = url
        self.company_type = company_type
        self.rank = None
        self.company_exchange_rates = None

    def set_rank_in_category(self, rank):
        self.rank = rank

    def set_exchange_rates(self, company_exchange_rates: List[CompanyExchangeRates]):
        self.company_exchange_rates = company_exchange_rates

    def add_exchange_rate(self, company_exchange_rate: CompanyExchangeRates):
        if self.company_exchange_rates is None:
            self.company_exchange_rates = []

        self.company_exchange_rates.append(company_exchange_rate)


def create_exchange_rate(currency: str, buy_rate=None, sell_rate=None) -> ExchangeRate |None:
    if is_float_ok(buy_rate) == False:
        buy_rate = None

    if is_float_ok(sell_rate) == False:
        sell_rate = None

    if buy_rate == None and sell_rate == None:
       return None

    return ExchangeRate(currency,buy_rate=buy_rate,sell_rate=sell_rate)