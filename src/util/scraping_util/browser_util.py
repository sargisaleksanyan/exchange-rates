import time

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from src.util.tool.proxy import get_random_proxy

ua = UserAgent()


def init_browser(url, wait_time=5, count=0) -> WebDriver | None:
    # enter_proxy_auth(proxy.user_name, proxy.password)
    browser = None
    try:
        chrome_options = webdriver.ChromeOptions()
        # TODO add proxy
      #  chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')

        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument(f'--user-agent={ua.chrome}')
        proxy = get_random_proxy()

        if (proxy is not None):
            chrome_options.add_argument('--proxy-server={}'.format(proxy.ip + ":" + proxy.port))
            #chrome_options.add_argument('--proxy-server=socks5://{}'.format(proxy.ip + ":" + proxy.port))
        browser = webdriver.Chrome(chrome_options)
        browser.get(url)

        time.sleep(wait_time)
        return browser
    except Exception as err:
        print(err)
        # TODO write logs
        close_browser(browser)
        if (count < 5):
            count = count + 1
            return init_browser(url, count)
    return None


def close_browser(browser: webdriver):
    try:
        browser.close()
    except Exception as err:
        print(err)


def get_website_content_by_browser(url, wait_time=5, count=0) -> str | None:
    browser = None
    try:
        browser = init_browser(url, wait_time, 0)
        page_source = browser.page_source
        browser.close()
        return page_source
    except Exception as err:
        close_browser(browser)
        if (count < 5):
            count = count + 1
            return get_website_content_by_browser(url, wait_time, count)
        return None


# TODO handle this function
def get_website_content_by_browser_by_visibilty_of_element(url, count=0) -> str | None:
    browser = None
    try:
        browser = init_browser(url)
        page_source = browser.page_source
        browser.close()
        return page_source
    except Exception as err:
        close_browser(browser)
        if (count < 5):
            count = count + 1
            return get_website_content_by_browser_by_visibilty_of_element(url, count)
        return None
