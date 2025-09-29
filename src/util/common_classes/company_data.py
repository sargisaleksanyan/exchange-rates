class BankName:
    FIRST_ABU_DHABI_BANK = 'First Abu Dhabi Bank'  # +
    EMIRATES_BANK = 'Emirates NBD'  # +
    ABU_DHABI_COMMERCIAL_BANK = 'Abu Dhabi Commercial Bank'  # +
    EMIRATES_ISLAMIC_BANK = 'Emirates Islamic Bank'  # +
    NATIONAL_BANK_OF_RAS_AL_KHAIMAH = 'National Bank of Ras Al-Khaimah'  # +
    COMMERCIAL_BANK_OF_DUBAI = 'Commercial Bank of Dubai'  # +
    SHARJAH_ISLAMIC_BANK = 'Sharjah Islamic Bank'  # +
    DUBAI_ISLAMIC_BANK = 'Dubai Islamic Bank'  # +
    AJMAN_BANK = 'AJMAN BANK'  # +
    NATIONAL_BANK_OF_FUJARAH = 'National Bank of Fujairah'

    MASHREQ_BANK = 'Mashreq Bank'  # No currency data was found
    ABU_DHABI_ISLAMIC_BANK = 'Abu Dhabi Islamic Bank (ADIB)'  # No currency data was found https://www.adib.ae/en/pages/currency-rates
    AL_HILAL_BANK = 'AL_HILAL_BANK'  # No info was found
    UNITED_ARAB_BANK = 'United Arab Bank'  # No information was found
    # 7 = 14


class BankUrl:
    ABU_DHABI_COMMERCIAL_BANK = 'adcb.com'  # +
    FIRST_ABU_DHABI_BANK = 'bankfab.com'  # +
    EMIRATES_BANK = 'emiratesnbd.com'  # +
    EMIRATES_ISLAMIC_BANK = 'emiratesislamic.ae'  # +
    DUBAI_ISLAMIC_BANK = 'dib.ae'
    NATIONAL_BANK_OF_RAS_AL_KHAIMAH = 'rakbank.ae'  # +
    NATIONAL_BANK_OF_FUJARAH = 'nbf.ae'
    COMMERCIAL_BANK_OF_DUBAI = 'cbd.ae'  # +
    SHARJAH_ISLAMIC_BANK = 'sib.ae'
    AJMAN_BANK = 'ajmanbank.ae'


class BankExchangeRateUrl:
    FIRST_ABU_DHABI_BANK = 'https://www.bankfab.com/en-ae/personal/fx-rate'
    EMIRATES_BANK = 'https://www.emiratesnbd.com/en/foreign-exchange'
    ABU_DHABI_COMMERCIAL_BANK = 'https://www.adcb.com/en/personal/accounts/money-transfer/fx-rate'
    EMIRATES_ISLAMIC_BANK = 'https://www.emiratesislamic.ae/en/personal-banking/foreign-currency/fx'
    DUBAI_ISLAMIC_BANK = 'https://www.dib.ae/exchange-rates'
    NATIONAL_BANK_OF_RAS_AL_KHAIMAH = 'https://www.rakbank.ae/en/everyday-banking/send-pay/foreign-exchange-rates'
    NATIONAL_BANK_OF_FUJARAH = 'https://nbf.ae/business/treasury-and-trading/foreign-exchange-rates'
    COMMERCIAL_BANK_OF_DUBAI = 'https://www.cbd.ae/islami/personal/investments-transfers/transfers'
    SHARJAH_ISLAMIC_BANK = 'https://www.sib.ae/en/exchange-rate-list'
    AJMAN_BANK = 'https://digitalbanking.ajmanbank.ae/ib-retail-web/user/exchangeRatesAndCurrencyConverter'


class BankExchangeRateApiUrl:
    EMIRATES_BANK = 'https://www.emiratesnbd.com/enbdapi/v1/currency/getexchangerates'
    EMIRATES_ISLAMIC_BANK = 'https://www.emiratesislamic.ae/eiapi/v1/Currency/GetAllCurrencies'
    NATIONAL_BANK_OF_RAS_AL_KHAIMAH = 'https://www.rakbank.ae/api/forex/rate'
    SHARJAH_ISLAMIC_BANK = 'https://www.sib.ae/classic/SIBCurrencyConvertor/GetCurrenciesData?currencyMarket=8&currencies='


class ExchangeBusinessUrl:
    AL_ANSARI_EXCHANGE = 'alansariexchange.com'
    AL_FARDAN_EXCHANGE = 'alfardanexchange.com'
    AL_ROSTAMANI_EXCHANGE = 'alrostamaniexchange.com'  # ?
    JOYALUKKAS_EXCHANGE = 'joyalukkasexchange.com'
    #
    LULU_EXCHANGE = 'luluexchange.com'  # Does not work
    WALL_STREET_EXCHANGE = 'wallstreet.ae'
    ORIENT_EXCHANGE = 'orientexchange.com'
    AL_GHURAIR_EXCHANGE = 'alghurairexchange.com'
    SHARAF_EXCHANGE = 'sharafexchange.ae'
    GCC_EXCHANGE = 'gccexchange.com'
    FEDERAL_EXCHANGE = 'federalexchange.ae'
    TRAVELEXAE = 'travelex.net'
    REDHA_AL_ANSARI_EXCHANGE = 'redhaalansari.com'
    NATIONAL_EXCHANGE_CO = 'nationalexc.com'
    INDEX_EXCHANGE = 'indexexchange.ae'
    AL_JARWAN_MONEY_EXCHANGE = 'aljarwanexchange.com'
    LARI_EXCHANGE = 'lariexchange.com'
    MESRKANLOO_INTERNATIONAL_EXCHANGE = 'mesrkanlooexchange.com'
    DINAR_EXCHANGE = 'dinarexchange.ae'
    REEMS_EXCHANGE = 'reems.ae'
    DESERT_EXCHANGE = 'desert-exchange.com'


class ExchangeBusinessNames:
    AL_ANSARI_EXCHANGE = 'Al Ansari Exchange'  # Diffcult have to scrape each currency one by one https://alansariexchange.com/service/foreign-exchange/
    AL_FARDAN_EXCHANGE = 'Al Fardan Exchange'  # https://alfardanexchange.com/  have to scrape on by one
    AL_ROSTAMANI_EXCHANGE = 'Al Rostamani Exchange'  # does not work at this moment
    JOYALUKKAS_EXCHANGE = 'Joyalukkas_Exchange'  # Seems to be working https://admin.joyalukkasexchange.com/api/country-currency-code https://admin.joyalukkasexchange.com/api/country-currency-code
    #                     https://admin.joyalukkasexchange.com/api/currency-converter?region=2&amount=1&currency_code=USD&rate_type=TT&amount_type=LCY for more detailed need to request one by one
    LULU_EXCHANGE = 'Lulu Exchange'  # Does not work
    WALL_STREET_EXCHANGE = 'Wall Street Exchange'  # https://www.wallstreet.ae/personal/foreign-exchange api https://www.wallstreet.ae/index.php/buy-sell?mode=buy_rate&isAjax=true
    ORIENT_EXCHANGE = ' Orient Exchange'  # https://www.orientexchange.com/Orient/GetSellRates                                 # https: // www.orientexchange.com / Orient / CurrencyRates
    AL_GHURAIR_EXCHANGE = 'Al Ghurair Exchange'  # https://3-214-76-133.nip.io/fc/0
    SHARAF_EXCHANGE = 'Sharaf Exchange'  # https://sharafexchange.ae/engine/wp-json/v1/currency-exchange-table-rates?lang=en
    GCC_EXCHANGE = 'GCC Exchange'  # https://www.gccexchange.com/media/index.php/exchangerate/getexchangerate - tansfers only
    FEDERAL_EXCHANGE = 'Federal Exchange',  # 'https://www.federalexchange.ae' shows tranfers rates
    TRAVELEXAE = 'Travelexae'  # https://api.travelex.net/salt/config/multi?callback=jQuery111008147785010350708_1758883151347&key=Travelex&site=%2Fae&options=abhikzl&_=1758883151348 only sell rates
    REDHA_AL_ANSARI_EXCHANGE = 'Redha Al-Ansari Exchange'  # Does not have any data
    NATIONAL_EXCHANGE_CO = 'National Exchange Co'  # 'https://nationalexc.com/how-it-works/' have only send money data
    INDEX_EXCHANGE = 'Index Exchange'  # https://www.indexexchange.ae/exchange_rates
    AL_JARWAN_MONEY_EXCHANGE = 'AL JARWAN MONEY EXCHANGE'  # https://aljarwanexchange.com
    LARI_EXCHANGE = 'Lari Exchange'  # https://www.lariexchange.com/Forex
    MESRKANLOO_INTERNATIONAL_EXCHANGE = 'Mesrkanloo International Exchange'  # https://mesrkanlooexchange.com/exchange-rate/ works !
    DINAR_EXCHANGE = 'Dinar Exchange'  # https: // dinarexchange.ae /
    REEMS_EXCHANGE = 'Reems Exchange'  # https://reems.ae/exchange-rates/
    DESERT_EXCHANGE = 'Desert Exchange'  # https://desert-exchange.com/services/foreign-currency-exchange/
    # https://unimoni.ae/ ??

    # https://www.goodwillexchange.ae/our-services did not understand if its own api


# ExchangeBusinessNames
class ExchangeBusinessExchangeUrl:
    def __init__(self):
        self.name = ''
