import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import Config

@pytest.fixture(scope='session')
def browser():
    options = Options()
    if Config.HEADLESS:
        options.add_argument("--headless")

    options.add_argument("--no-sandbox")
    options.add_argument(f"--window-size={Config.BROWSER_WIDTH},{Config.BROWSER_HEIGHT}")

    chrome_browser = webdriver.Chrome(options=options)
    chrome_browser.implicitly_wait(Config.DEFAULT_TIMEOUT)

    yield chrome_browser
    chrome_browser.quit()


@pytest.fixture
def base_url():
    return Config.get_ui_url()

