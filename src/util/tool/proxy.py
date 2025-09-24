from random import randrange

from src.util.common_classes import filename_holder

proxies = []


class Proxy:
    def __init__(self, ip, port, user_name, password):
        self.ip = ip
        self.port = port
        self.user_name = user_name
        self.password = password


def getProxies():
    if (len(proxies) > 0):
        return proxies

    proxyData = open(filename_holder.FileNames.proxyFileName, 'r+')
    for proxyText in proxyData:
        values = proxyText.split(':')
        proxy = Proxy(values[0], values[1], values[2], values[3])
        proxies.append(proxy)

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

        return {
            # "https": 'https://' + proxy.userName + ":" + proxy.password + "@" + proxy.ip + ":" + proxy.port,
            # "http": 'http://' + proxy.userName + ":" + proxy.password + "@" + proxy.ip + ":" + proxy.port
            "http": proxy.user_name + ":" + proxy.password + "@" + proxy.ip + ":" + proxy.port,
            "https": proxy.user_name + ":" + proxy.password + "@" + proxy.ip + ":" + proxy.port
        }

    return None
