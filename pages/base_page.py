from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from typing import Tuple, Optional
from config import Config

class BasePage:
    def __init__(self, browser: WebDriver) -> None:
        self.browser = browser
        self.wait = WebDriverWait(browser, Config.DEFAULT_TIMEOUT, poll_frequency=Config.POLL_FREQUENCY)
        self.actions = ActionChains(browser)

    def open_url(self, url: str) -> None:
        self.browser.get(url)

    def find(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        wait = self.wait if timeout is None else WebDriverWait(self.browser, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def find_clickable(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        wait = self.wait if timeout is None else WebDriverWait(self.browser, timeout)
        return wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        element = self.find_clickable(locator, timeout)
        element.click()
        return element

    def is_visible(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        try:
            wait = self.wait if timeout is None else WebDriverWait(self.browser, timeout)
            return wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def is_present(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        try:
            wait = self.wait if timeout is None else WebDriverWait(self.browser, timeout)
            wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def enter_text(self, locator: Tuple[str, str], text: str, clear_first: bool = True) -> WebElement:
        element = self.find(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
        return element

    def get_text(self, locator: Tuple[str, str]) -> str:
        return self.find(locator).text

    def get_value(self, locator: Tuple[str, str]) -> str:
        return self.find(locator).get_attribute('value')

    def wait_for_invisibility(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        wait = self.wait if timeout is None else WebDriverWait(self.browser, timeout)
        return wait.until(EC.invisibility_of_element_located(locator))

    def alert_is_present(self, timeout: Optional[int] = None) -> Optional[str]:
        try:
            wait = self.wait if timeout is None else WebDriverWait(self.browser, timeout)
            alert = wait.until(EC.alert_is_present())
            text = alert.text
            alert.accept()
            return text
        except (NoAlertPresentException, TimeoutException):
            return None