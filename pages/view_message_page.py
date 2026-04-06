from .base_page import BasePage
from utils.locators import Locators
from typing import Optional

class ViewMessagePage(BasePage):
    def __init__(self, browser):
        super().__init__(browser)
        self.locators = Locators()

    def enter_pin(self, pin) -> "ViewMessagePage":
        self.enter_text(self.locators.PIN_UNLOCK, str(pin))
        return self
    
    def click_submit(self) -> "ViewMessagePage":
        self.click(self.locators.BUTTON_RETRIEVE)
        return self

    def open_secret(self, url, pin=None) -> "ViewMessagePage":
        self.open_url(url)
        self.enter_pin(pin)
        self.click_submit()
        return self
    
    def has_text(self) -> bool:
        return self.is_visible(self.locators.MESSAGE_AREA, timeout=3)

    def has_file(self) -> bool:
        return self.is_visible(self.locators.FILE_NAME, timeout=3)

    def get_secret_text(self) -> Optional[str]:
        try:
            return self.get_text(self.locators.MESSAGE_AREA)
        except:
            return None
        
    def verify_text(self, expected_text) -> bool:
        actual_text = self.get_secret_text()
        return actual_text == expected_text
    