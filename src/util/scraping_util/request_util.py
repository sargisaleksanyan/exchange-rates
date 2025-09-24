import requests
from fake_useragent import UserAgent

from src.util.tool.proxy import get_random_proxy, get_random_proxy_for_request

MAX_REQUEST = 5


def make_get_request_with_proxy(url: str, request_count=0):
    headers = {
        'user-agent': UserAgent().chrome,
        'timeout': '10',
        'referer': url
    }

    try:
        proxies = get_random_proxy_for_request()
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


def make_post_request_with_proxy(url: str, body, is_url_encoded=False, request_count=0):
    headers = {
        'user-agent': UserAgent().chrome,
        'timeout': '10',
        'referer': url
    }

    if is_url_encoded == True:
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

    try:
        proxies = get_random_proxy_for_request()
        response = requests.post(url, data=body, headers=headers, proxies=proxies, timeout=10)
        content = response.content
        response.close()
        return content
    except Exception as err:
        print('Error', err, ' Url', url)
        if (request_count < MAX_REQUEST):
            request_count = request_count + 1
            return make_post_request_with_proxy(url, request_count=request_count)
        else:
            return None
