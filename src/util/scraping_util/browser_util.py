import time

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from src.util.tool.proxy import get_random_proxy

ua = UserAgent()


def init_browser(url, wait_time=5, count=0) -> WebDriver | None:
    # enter_proxy_auth(proxy.user_name, proxy.password)

    try:
        chrome_options = webdriver.ChromeOptions()
        # TODO add proxy
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')

        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument(f'--user-agent={ua.chrome}')
        proxy = get_random_proxy()

        if (proxy is not None):
            chrome_options.add_argument('--proxy-server={}'.format(proxy.ip + ":" + proxy.port))
        browser = webdriver.Chrome(chrome_options)
        browser.get(url)

        time.sleep(wait_time)
        return browser
    except Exception as err:
        print(err)
        # TODO write logs
        if (count < 5):
            count = count + 1
            init_browser(url, count)
    return None


def get_website_content_by_browser(url, wait_time=5, count=0) -> str | None:
    try:
        browser = init_browser(url, wait_time, 0)
        page_source = browser.page_source
        browser.close()
        return page_source
    except Exception as err:
        init_browser(0)
        if (count < 5):
            count = count + 1
            get_website_content_by_browser(url, wait_time, count)
        return None


# TODO handle this function
def get_website_content_by_browser_by_visibilty_of_element(url, count=0) -> str | None:
    try:
        browser = init_browser(url)
        page_source = browser.page_source
        browser.close()
        return page_source
    except Exception as err:
        init_browser(0)
        if (count < 5):
            count = count + 1
            get_website_content_by_browser(url, count)
        return None
