from src.util.scraping_util.request_util import make_get_request_with_proxy


def scrape_data():
    content = make_get_request_with_proxy('https://masarif.ae/banks')
    m  = 5


scrape_data()
