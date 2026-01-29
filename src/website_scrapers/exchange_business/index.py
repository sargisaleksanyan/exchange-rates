from src.website_scrapers.exchange_business.al_ansari_exchange import scrape_al_ansari_exchange
from src.website_scrapers.exchange_business.al_ghurair import scrape_al_ghurair
from src.website_scrapers.exchange_business.dar_exchange import scrape_dar_exchange
from src.website_scrapers.exchange_business.desert_exchange import scrape_desert_exchange
from src.website_scrapers.exchange_business.index_exchange import scrape_index_exchange
from src.website_scrapers.exchange_business.joyalukkas import scrape_joyalukkas_exchange
from src.website_scrapers.exchange_business.orient_exchange import scrape_orient_exchange
from src.website_scrapers.exchange_business.reems import scrape_reems_exchange
from src.website_scrapers.exchange_business.send_exchange import scrape_send_exchange

very_rearly_exchange_update = [scrape_joyalukkas_exchange,scrape_al_ansari_exchange]
non_frequent_currency_exchange_update = [scrape_orient_exchange, scrape_al_ghurair]
frequent_currency_exchange_update = [#scrape_wall_street,removed wall street   
                                     scrape_desert_exchange, scrape_index_exchange,
                                     scrape_dar_exchange,
                                     scrape_send_exchange,
                                     scrape_reems_exchange]

