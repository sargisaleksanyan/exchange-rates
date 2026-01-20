class BankName:
    FIRST_ABU_DHABI_BANK = 'First Abu Dhabi Bank'  # +
    EMIRATES_BANK = 'Emirates NBD'  # +
    ABU_DHABI_COMMERCIAL_BANK = 'Abu Dhabi Commercial Bank'  # +
    EMIRATES_ISLAMIC_BANK = 'Emirates Islamic Bank'  # +
    NATIONAL_BANK_OF_RAS_AL_KHAIMAH = 'National Bank of Ras Al-Khaimah'  # +
    COMMERCIAL_BANK_OF_DUBAI = 'Commercial Bank of Dubai'  # +
    SHARJAH_ISLAMIC_BANK = 'Sharjah Islamic Bank'  # +
    DUBAI_ISLAMIC_BANK = 'Dubai Islamic Bank'  # +
    AJMAN_BANK = 'Ajman Bank'  # +
    NATIONAL_BANK_OF_FUJARAH = 'National Bank of Fujairah'  # +
    ABU_DHABI_ISLAMIC_BANK = 'Abu Dhabi Islamic Bank (ADIB)'  # + https://www.adib.com/en/pages/currency-rates.aspx
    NATIONAL_BANK_OF_UMM_AL_QAIWAIN = 'National Bank of Umm Al-Qaiwain'  # + https://nbq.ae/general/fcy-rate-list can scrape it

    BANK_OF_SHARJAH = 'Bank of Sharjah'  # can be scraped  Have anti scraping system

    AL_HILAL_BANK = 'Al Hilal Bank'  # ? this seems to be part of adcb.com
    AL_MARYAH_COMMUNITY_BANK = 'Al Maryah Community Bank'  # No data is shown
    RUYA_COMMUNITY_ISLAMIC_BANK = 'Ruya Community Islamic Bank'  # Did not find any data
    EMIRATES_INVESTMENT_BANK = 'Emirates Investment Bank'  # investment bank , does mot have exchage data
    COMMERCIAL_BANK_INTERNATIONAL = 'Commercial Bank International'  # no info was found
    MASHREQ_BANK = 'Mashreq Bank'  # No currency data was found
    UNITED_ARAB_BANK = 'United Arab Bank'  # No information was found
    AL_HILAL_BANK = 'AL_HILAL_BANK'  # No info was found

    # International
    BNP_PARIBAS_MIDDLE_EAST_AND_AFRICA_AUE = 'BNP Paribas Middle East and; Africa UAE'
    # 7 = 14


class BankUrl:
    ABU_DHABI_COMMERCIAL_BANK = 'adcb.com'  # +
    ABU_DHABI_ISLAMIC_BANK = 'adib.com'  # +
    AJMAN_BANK = 'ajmanbank.ae'  # +
    BANK_OF_SHARJAH = 'bankofsharjah.com'
    AL_MARYAH_COMMUNITY_BANK = 'mbank.ae'  # No data is shown
    FIRST_ABU_DHABI_BANK = 'bankfab.com'  # +
    EMIRATES_BANK = 'emiratesnbd.com'  # +
    EMIRATES_ISLAMIC_BANK = 'emiratesislamic.ae'  # +
    DUBAI_ISLAMIC_BANK = 'dib.ae'
    NATIONAL_BANK_OF_RAS_AL_KHAIMAH = 'rakbank.ae'  # +
    NATIONAL_BANK_OF_FUJARAH = 'nbf.ae'
    COMMERCIAL_BANK_OF_DUBAI = 'cbd.ae'  # +
    SHARJAH_ISLAMIC_BANK = 'sib.ae'
    NATIONAL_BANK_OF_UMM_AL_QAIWAIN = 'nbq.ae'
    # International
    BNP_PARIBAS_MIDDLE_EAST_AND_AFRICA_AUE = 'bnpparibas.com'


class BankExchangeRateUrl:
    ABU_DHABI_ISLAMIC_BANK = 'https://www.adib.com/en/pages/currency-rates.aspx'
    FIRST_ABU_DHABI_BANK = 'https://www.bankfab.com/en-ae/personal/fx-rate'
    EMIRATES_BANK = 'https://www.emiratesnbd.com/en/foreign-exchange'
    BANK_OF_SHARJAH = 'https://www.bankofsharjah.com/en/rates'
    ABU_DHABI_COMMERCIAL_BANK = 'https://www.adcb.com/en/personal/accounts/money-transfer/fx-rate'
    EMIRATES_ISLAMIC_BANK = 'https://www.emiratesislamic.ae/en/personal-banking/foreign-currency/fx'
    DUBAI_ISLAMIC_BANK = 'https://www.dib.ae/exchange-rates'
    NATIONAL_BANK_OF_RAS_AL_KHAIMAH = 'https://www.rakbank.ae/en/everyday-banking/send-pay/foreign-exchange-rates'
    NATIONAL_BANK_OF_FUJARAH = 'https://nbf.ae/business/treasury-and-trading/foreign-exchange-rates'
    COMMERCIAL_BANK_OF_DUBAI = 'https://www.cbd.ae/islami/personal/investments-transfers/transfers'
    # https://www.cbd.ae/islami/personal/investments-transfers/international-transfers-swift
    SHARJAH_ISLAMIC_BANK = 'https://www.sib.ae/en/exchange-rate-list'
    AJMAN_BANK = 'https://digitalbanking.ajmanbank.ae/ib-retail-web/user/exchangeRatesAndCurrencyConverter'
    NATIONAL_BANK_OF_UMM_AL_QAIWAIN = 'https://nbq.ae/general/fcy-rate-list'

    # International
    BNP_PARIBAS_MIDDLE_EAST_AND_AFRICA_AUE = 'https://mea.bnpparibas.com/en/live-fx-rates/live-fx-rates-auh'


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
    ONYX_EXCHANGE = 'onyx-exchange.com'  # Onyx Exchange
    DAR_EXCHANGE = 'darexchange.com'
    OMDA_EXCHANGE = 'Omda Exchange'
    SEND_EXCHANGE = 'sendexchange.com'


# https://capitalexchange.ae/


class ExchangeBusinessNames:
    AL_ANSARI_EXCHANGE = 'Al Ansari Exchange'  # Diffcult have to scrape each currency one by one https://alansariexchange.com/service/foreign-exchange/
    AL_FARDAN_EXCHANGE = 'Al Fardan Exchange'  # https://alfardanexchange.com/  https://alfardanexchange.com/foreign-exchange
    AL_ROSTAMANI_EXCHANGE = 'Al Rostamani Exchange'  # does not work at this moment
    JOYALUKKAS_EXCHANGE = 'Joyalukkas Exchange'  # Seems to be working https://admin.joyalukkasexchange.com/api/country-currency-code https://admin.joyalukkasexchange.com/api/country-currency-code
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
    LARI_EXCHANGE = 'Lari Exchange'  # https://www.lariexchange.com/Forex not easy to scrape , Only provides transfer rates in bulk
    MESRKANLOO_INTERNATIONAL_EXCHANGE = 'Mesrkanloo International Exchange'  # https://mesrkanlooexchange.com/exchange-rate/ takes rates from https://efastlive.com Do not think need it
    DINAR_EXCHANGE = 'Dinar Exchange'  # https: // dinarexchange.ae /
    REEMS_EXCHANGE = 'Reems Exchange'  # https://reems.ae/exchange-rates/
    DESERT_EXCHANGE = 'Desert Exchange'  # https://desert-exchange.com/services/foreign-currency-exchange/
    ##################################
    ONYX_EXCHANGE = 'Onyx Exchange'
    DAR_EXCHANGE = 'Dar Exchange'
    OMDA_EXCHANGE = 'Omda exchange'
    SEND_EXCHANGE = 'Send Exchange'


# 'https://sendexchange.com/'


# https://unimoni.ae/ ??

# https://www.goodwillexchange.ae/our-services did not understand if its own api


# ExchangeBusinessNames
class ExchangeBusinessExchangeUrl:
    JOYALUKKAS_EXCHANGE = 'joyalukkasexchange.com'  # 1 +
    WALL_STREET_EXCHANGE = 'wallstreet.ae/personal/foreign-exchange'  # 2 +
    ORIENT_EXCHANGE = 'orientexchange.com/Orient/CurrencyRates'  # 3  +
    AL_GHURAIR_EXCHANGE = 'alghurairexchange.com'  # + 5 https://3-214-76-133.nip.io/fc/0
    DESERT_EXCHANGE = 'https://desert-exchange.com/currency-buy-sell'  # 8 +
    DAR_EXCHANGE = 'https://darexchange.com/foreign-currencies-exchange'  # + 6 but transfer seems to show incorrect info
    REEMS_EXCHANGE = 'https://reems.ae/exchange-rates'  # 7 +
    SEND_EXCHANGE = 'https://sendexchange.com'  # +

    GCC_EXCHANGE = 'https://www.gccexchange.com/uae-currency-exchange-rates'  # only tranfers
    OMDA_EXCHANGE = 'https://omdaexchange.com/service/foreign-currency-exchange/'  # shows very old data
    AL_FARDAN_EXCHANGE = 'alfardanexchange.com/foreign-exchange'  # 4 Rates are in reverse order # seems to have bug shows incorrect or negative rates need to get one by one
    INDEX_EXCHANGE = 'https://www.indexexchange.ae/exchange_rates'  # 6 shows both sell and buy but seems to show transfer incorrectly +
    #AL_ANSARI_EXCHANGE = 'https://app.eexchange.ae/eExchange/login/loadChargesAndRatePage.action'  # ? 5 Transfer Rates only for each currency have to get once by once https://alansariexchange.com/service/foreign-exchange/
    AL_ANSARI_EXCHANGE = 'https://alansariexchange.com/service/foreign-exchange'  # ? 5 Transfer Rates only for each currency have to get once by once https://alansariexchange.com/service/foreign-exchange/


class ExchangeBusinessApiUrl:
    JOYALUKKAS_EXCHANGE = 'https://admin.joyalukkasexchange.com/api/country-currency-code'
    WALL_STREET_EXCHANGE = 'https://www.wallstreet.ae/index.php/buy-sell?mode=buy_rate&isAjax=true'
    SHARAF_EXCHANGE = 'https://sharafexchange.ae/engine/wp-json/v1/currency-exchange-table-rates?lang=en'
    ORIENT_EXCHANGE_SELL_RATES = 'https://www.orientexchange.com/Orient/GetSellRates'
    ORIENT_EXCHANGE_BUY_RATES = 'https://www.orientexchange.com/Orient/GetBuyRates'
    ORIENT_EXCHANGE_TRANSFER = 'https://www.orientexchange.com/Orient/GetExchangeRates'
    AL_GHURAIR_EXCHANGE_CASH_RATES = 'https://3-214-76-133.nip.io/fc/0'  # https://3-214-76-133.nip.io/tt/0
    AL_GHURAIR_EXCHANGE_TRANSFER_RATES = 'https://3-214-76-133.nip.io/tt/0'
