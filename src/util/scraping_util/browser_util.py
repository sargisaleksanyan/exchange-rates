import time

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from src.util.tool.proxy import get_random_proxy

ua = UserAgent()


# sudo apt-get install python3-tk python3-dev todo in server
def enter_proxy_auth(proxy_username, proxy_password):
    try:
        time.sleep(1)
        # pyautogui.typewrite(proxy_username)
        # pyautogui.press('tab')
        # pyautogui.typewrite(proxy_password)
        # pyautogui.press('enter')
    except Exception as err:
        print('Error during entering proxy auth ', err)


def init_browser(url, count=0) -> WebDriver | None:
    chrome_options = webdriver.ChromeOptions()
    # TODO add proxy
    # chrome_options.add_argument('--proxy-server=%s' % proxy)

    chrome_options.add_argument('--headless')
    chrome_options.add_argument(f'--user-agent={ua.chrome}')
    # proxy = get_random_proxy()

    # if (proxy is not None):
    # chrome_options.add_argument('--proxy-server={}'.format(proxy.ip + ":" + proxy.port))
    # enter_proxy_auth(proxy.user_name, proxy.password)

    try:
        browser = webdriver.Chrome(chrome_options)
        time.sleep(5)

        # if (proxy is not None):
        # chrome_options.add_argument('--proxy-server={}'.format(proxy.ip + ":" + proxy.port))
        # enter_proxy_auth(proxy.user_name, proxy.password)

        browser.get(url)
        time.sleep(5)
        return browser
    except Exception as err:
        print(err)
        if (count < 5):
            count = count + 1
            init_browser(url, count)
    return None


def get_website_content_by_browser(url, count=0) -> str | None:
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
