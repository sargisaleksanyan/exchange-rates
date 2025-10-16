from datetime import datetime
from enum import Enum
from typing import List


class Currency(Enum):
    AUD = ("AUD", "Australian Dollar")
    BHD = ("BHD", "Bahraini Dinar")
    CAD = ("CAD", "Canadian Dollar")
    CYP = ("CYP", "Cyprus Pound")
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
    #AZM = ("AZM", "Azerbaijani Manat") # TODO real name is AZN , need to convert AZM to AZN the old one
    MVR = ("MVR","Maldivian Rufiyaa")
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
    TND = ("TND", "Tunisian Dinar")
    TZS = ("TZS", "Tanzanian Shilling")
    TJS = ("TJS", "Tajikistani Somoni")
    TWD = ("TWD", "New Taiwan Dollar")
    SYP = ("SYP", "Syrian Pound")
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
    ###############################
    AFN = ("AFN", "Afghan Afghani")
    ALL = ("ALL", "Albanian Lek")
    ANG = ("ANG", "Netherlands Antillean Guilder")
    AOA = ("AOA", "Angolan Kwanza")
    BGN = ("BGN", "Bulgarian Lev")
    BND = ("BND", "Brunei Dollar")
    BOB = ("BOB", "Bolivian Boliviano")
    BAM = ("BAM","Bosnia and Herzegovina convertible mark")
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

    def __init__(self, code, fullname):
        self.code = code
        self.fullname = fullname

    def __str__(self):
        return f"{self.code} - {self.fullname}"

    def get_currency(currency):
        if (currency is None):
            return None
        if isinstance(currency, Currency):
            return Currency[currency]
        if isinstance(currency, str) and currency in Currency._value2member_map_ or currency in (c.code for c in
                                                                                                 Currency):
            return Currency[currency]

        print('Currency has not been found', currency)  # TODO print this
        return None


class ExchangeCompanyType(Enum):
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
        self.buy_rate = buy_rate
        self.sell_rate = sell_rate
        self.rate = rate
        self.exchange_type = None
        self.update_date = None

    def set_exchange_type(self, exchange_type: ExchangeType):
        self.exchange_type = exchange_type

    def set_update_date(self, update_date):
        self.update_date = update_date


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
        self.update_date = update_date

    def set_scrape_date(self, scrape_date):
        self.scrape_date = scrape_date

    def set_current_scrape_date(self):
        self.scrape_date = datetime.now()


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
