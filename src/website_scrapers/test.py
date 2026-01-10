import requests

from src.util.scraping_util.request_util import make_get_request_with_proxy
from src.util.tool.proxy import get_random_proxy_for_request


def test_ip():
    n = 1
    print('response test ip')

    proxies = get_random_proxy_for_request()

    # Send request through the proxy to check your public IP
    # The timeout prevents the script from hanging if the proxy is slow/dead
    resp = requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=10)

    response = make_get_request_with_proxy('https://api.ipify.org?format=json')
    print(response)
    m = 5


test_ip()
