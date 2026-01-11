from random import randrange
from urllib.parse import quote

from src.util.common_classes import filename_holder

proxies = []


class Proxy:
    def __init__(self, ip, port, user_name=None, password=None):
        self.ip = ip
        self.port = port
        self.user_name = user_name
        self.password = password


def clean_string(string: str):
    if string == None:
        return string
    return string.replace("\n", "").strip()


def getProxies():
    if (len(proxies) > 0):
        return proxies

    proxyData = open(filename_holder.FileNames.proxyFileName, 'r+')
    for proxyText in proxyData:
        values = proxyText.split(':')
        if (len(values) > 3):
            proxy = Proxy(clean_string(values[0]), clean_string(values[1]), quote(clean_string(values[2])),
                          quote(clean_string(values[3])))
            proxies.append(proxy)
        elif len(values) == 2:
            proxies.append(Proxy(clean_string(values[0]), clean_string(values[1])))

    proxyData.close()
    return proxies


proxy_list = getProxies()


def get_random_proxy() -> Proxy | None:
    if len(proxy_list) > 0:
        proxy = proxy_list[0]

        if (len(proxy_list) > 1):
            proxy = proxy_list[randrange(0, len(proxy_list) - 1)]
            return proxy

        return proxy
    return None


def get_random_proxy_for_request():
    if len(proxy_list) > 0:
        proxy = proxy_list[0]

        if (len(proxy_list) > 1):
            proxy = proxy_list[randrange(0, len(proxy_list) - 1)]

        if (proxy.user_name is not None and proxy.password is not None):
            return {
                "https": f"http://{proxy.user_name}:{proxy.password}@{proxy.ip}:{proxy.port}",
                "http": f"http://{proxy.user_name}:{proxy.password}@{proxy.ip}:{proxy.port}",
                # "socks5": "socks5://" + proxy.user_name + ":" + proxy.password + "@" + proxy.ip + ":" + proxy.port,
                #"http": "https://" + proxy.user_name + ":" + proxy.password + "@" + proxy.ip + ":" + proxy.port
            }
        else:
            return {
                "https": "https://" + proxy.ip + ":" + proxy.port,
                # "socks5": "socks5://" + proxy.ip + ":" + proxy.port,
                # "http": "socks5://" + proxy.ip + ":" + proxy.port
                "http": "http://" + proxy.ip + ":" + proxy.port
            }

    return None
