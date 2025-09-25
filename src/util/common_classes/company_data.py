class BankName:
    FIRST_ABU_DHABI_BANK = 'First Abu Dhabi Bank' #
    EMIRATES_BANK = 'Emirates NBD' #
    ABU_DHABI_COMMERCIAL_BANK = 'Abu Dhabi Commercial Bank'#
    EMIRATES_ISLAMIC_BANK = 'Emirates Islamic Bank'#
    DUBAI_ISLAMIC_BANK = 'Dubai Islamic Bank'
    NATIONAL_BANK_OF_RAS_AL_KHAIMAH = 'National Bank of Ras Al-Khaimah'#
    NATIONAL_BANK_OF_FUJARAH = 'National Bank of Fujairah'
    COMMERCIAL_BANK_OF_DUBAI = 'Commercial Bank of Dubai'
    SHARJAH_ISLAMIC_BANK = 'Sharjah Islamic Bank'


class BankUrl:
    FIRST_ABU_DHABI_BANK = 'bankfab.com'  # +
    EMIRATES_BANK = 'emiratesnbd.com'  # +
    ABU_DHABI_COMMERCIAL_BANK = 'adcb.com'  # +
    EMIRATES_ISLAMIC_BANK = 'emiratesislamic.ae'  # +
    DUBAI_ISLAMIC_BANK = 'dib.ae'
    NATIONAL_BANK_OF_RAS_AL_KHAIMAH = 'rakbank.ae'  # +
    NATIONAL_BANK_OF_FUJARAH = 'nbf.ae'
    COMMERCIAL_BANK_OF_DUBAI = 'cbd.ae' # +
    SHARJAH_ISLAMIC_BANK = 'sib.ae'


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


class BankExchangeRateApiUrl:
    EMIRATES_BANK = 'https://www.emiratesnbd.com/enbdapi/v1/currency/getexchangerates'
    EMIRATES_ISLAMIC_BANK = 'https://www.emiratesislamic.ae/eiapi/v1/Currency/GetAllCurrencies'
    NATIONAL_BANK_OF_RAS_AL_KHAIMAH = 'https://www.rakbank.ae/api/forex/rate'
    SHARJAH_ISLAMIC_BANK = 'https://www.sib.ae/classic/SIBCurrencyConvertor/GetCurrenciesData?currencyMarket=8&currencies='
