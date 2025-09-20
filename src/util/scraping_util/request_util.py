import requests
from fake_useragent import UserAgent

from src.util.tool.proxy import get_random_proxy

MAX_REQUEST = 5


def make_get_request_with_proxy(url: str, request_count=0):
    headers = {
        'user-agent': UserAgent().chrome,
        'timeout': '10',
        'referer': url
    }

    try:
        proxies = get_random_proxy()
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        content = response.content
        response.close()
        return content
    except Exception as err:
        print('Error', err, ' Url', url)
        if (request_count < MAX_REQUEST):
            request_count = request_count + 1
            return make_get_request_with_proxy(url, request_count)
        else:
            return None
