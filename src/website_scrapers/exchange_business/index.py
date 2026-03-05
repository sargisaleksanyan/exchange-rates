from src.website_scrapers.exchange_business.al_ahalia_exchange import scrape_al_ahalia_exchange
from src.website_scrapers.exchange_business.al_ansari_exchange import scrape_al_ansari_exchange
from src.website_scrapers.exchange_business.al_dahab_exchange import scrape_al_dahab_exchange
from src.website_scrapers.exchange_business.al_fardan_exchange import scrape_al_fardan
from src.website_scrapers.exchange_business.al_fuade_exchange import scrape_al_fuade
from src.website_scrapers.exchange_business.al_ghurair import scrape_al_ghurair
from src.website_scrapers.exchange_business.dar_exchange import scrape_dar_exchange
from src.website_scrapers.exchange_business.desert_exchange import scrape_desert_exchange
from src.website_scrapers.exchange_business.federal_exchange import scrape_federal_exchange
from src.website_scrapers.exchange_business.gcc_exchange import scrape_gcc_exchange
from src.website_scrapers.exchange_business.hadi_exchange import scrape_hadi_exchange
from src.website_scrapers.exchange_business.index_exchange import scrape_index_exchange
from src.website_scrapers.exchange_business.joyalukkas import scrape_joyalukkas_exchange
from src.website_scrapers.exchange_business.mesrkanloo_International_exchange import \
    scrape_mesrkanloo_international_exchange
from src.website_scrapers.exchange_business.multinet_trust_exchange import scrape_multinet_trust
from src.website_scrapers.exchange_business.orient_exchange import scrape_orient_exchange
from src.website_scrapers.exchange_business.reems import scrape_reems_exchange
from src.website_scrapers.exchange_business.send_exchange import scrape_send_exchange
from src.website_scrapers.exchange_business.sharaf_exchange import scrape_sharaf_exchange

very_rearly_exchange_update = [scrape_joyalukkas_exchange, scrape_al_ansari_exchange]
non_frequent_currency_exchange_update = [scrape_orient_exchange, scrape_al_fardan

                                         ]
frequent_currency_exchange_update = [  # scrape_wall_street,removed wall street
    scrape_al_fuade,
    scrape_al_ghurair,
    scrape_al_ahalia_exchange,
    scrape_al_dahab_exchange,
    scrape_al_fuade,
    scrape_dar_exchange,
    scrape_desert_exchange,
    scrape_gcc_exchange,
    scrape_multinet_trust,
    scrape_mesrkanloo_international_exchange,
    scrape_index_exchange,
    scrape_send_exchange,
    scrape_sharaf_exchange,
    scrape_reems_exchange,
    scrape_hadi_exchange,
    scrape_federal_exchange
]
