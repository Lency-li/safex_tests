from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from config import Config



class BasePage:
    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(browser, Config.DEFAULT_TIMEOUT, poll_frequency=Config.POLL_FREQUENCY)
        self.actions = ActionChains(browser)
    
    def open_url(self, url):
        self.browser.get(url)
    
    def find(self, locator, timeout=None):
        wait = self.wait if timeout is None else WebDriverWait(self.browser, timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def find_clickable(self, locator, timeout=None):
        wait = self.wait if timeout is None else WebDriverWait(self.browser, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def click(self, locator, timeout=None):
        element = self.find_clickable(locator, timeout)
        element.click()
        return element
    
    def is_visible(self, locator, timeout=None):
        try:
            wait = self.wait if timeout is None else WebDriverWait(self.browser, timeout)
            return wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False
    
    def is_present(self, locator, timeout=None):
        try:
            wait = self.wait if timeout is None else WebDriverWait(self.browser, timeout)
            wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def enter_text(self, locator, text, clear_first=True):
        element = self.find(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
        return element
    
    def get_text(self, locator):
        return self.find(locator).text
    
    def get_value(self, locator):
        return self.find(locator).get_attribute('value')
    
    def wait_for_invisibility(self, locator, timeout=None):
        wait = self.wait if timeout is None else WebDriverWait(self.browser, timeout)
        return wait.until(EC.invisibility_of_element_located(locator))
    
    def alert_is_present(self, timeout=None):
        try:
            wait = self.wait if timeout is None else WebDriverWait(self.browser, timeout)
            alert = wait.until(EC.alert_is_present())
            text = alert.text
            alert.accept()
            return text
        except (NoAlertPresentException, TimeoutException):
            return None