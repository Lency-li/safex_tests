from .base_page import BasePage
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from utils.locators import Locators
from config import Config
from typing import Optional, Union, Any



class CreateMessagePage(BasePage):
    def __init__(self, browser):
        super().__init__(browser)
        self.locators = Locators()

    def open(self) -> None:
        self.open_url(Config.BASE_URL)

    def is_text_area_visible(self) -> bool:
        return self.is_visible(self.locators.TEXT_AREA)
    
    def is_pin_input_visible(self) -> bool:
        return self.is_visible(self.locators.PIN_INPUT)
    
    def is_submit_enabled(self) -> bool:
        return self.find(self.locators.SUBMIT_BUTTON).is_enabled()
    
    def is_file_zone_enabled(self, timeout=5) -> bool:
        return self.is_visible(self.locators.FILE_LABEL, timeout)
    
    def set_text(self, text) -> Any:
        return self.enter_text(self.locators.TEXT_AREA, text)
    
    def set_pin(self, pin) -> Any:
        return self.enter_text(self.locators.PIN_INPUT, str(pin))
    
    def set_duration(self, index=0) -> "CreateMessagePage":
        self.click(self.locators.SELECT_UNIT)
        select = Select(self.find(self.locators.SELECT_UNIT))
        select.select_by_index(index)
        return self
    
    def set_duration_by_value(self, value) -> "CreateMessagePage":
        self.click(self.locators.SELECT_UNIT)
        select = Select(self.find(self.locators.SELECT_UNIT))
        select.select_by_value(value)
        return self
    
    def set_ttl(self, ttl=15) -> Any:
        return self.enter_text(self.locators.EXPIRY_VALUE, str(ttl))
    
    def activate_file_upload(self) -> "CreateMessagePage":
        self.browser.execute_script("""
            document.getElementById('secret-message').value = '';
            
            var fileInput = document.getElementById('secret-file');
            fileInput.disabled = false;
            fileInput.classList.remove('hidden');
            
            var dropzone = document.getElementById('secret-file-dropzone');
            dropzone.classList.remove('opacity-50', 'pointer-events-none');
            dropzone.removeAttribute('aria-disabled');
        """)
        
        self.wait.until(
            lambda driver: driver.execute_script(
                "return document.getElementById('secret-file').disabled === false;"
            )
        )
        return self
    
    def upload_file(self, file_path) -> bool:
        self.activate_file_upload()
        
        file_input = self.find(self.locators.FILE_INPUT)
            
        file_input.send_keys(file_path)
        
        try:
            self.wait.until(
                EC.visibility_of_element_located((By.ID, "secret-file-info"))
            )
            return True
        except TimeoutException:
            return False

    
    def click_submit(self) -> "CreateMessagePage":
        self.click(self.locators.SUBMIT_BUTTON)
        return self

    def clear_form(self) -> "CreateMessagePage":
        self.set_text("")
        self.set_pin("")
        self.set_ttl(15)
        self.set_duration_by_value("minutes")
        return self
    
    def get_link_text(self) -> str:
        return self.get_text(self.locators.LINK_RESULT)
    
    def copy_link(self) -> "CreateMessagePage":
        self.click(self.locators.COPY_BUTTON)
        return self

    def create_message(
        self,
        text: Optional[str] = None,
        file_path: Optional[str] = None,
        pin: Optional[Union[str, int]] = None,
        ttl: int = 15,
        duration: str = "minutes"
    ) -> Optional[str]:
        self.clear_form()
        if text:
            self.set_text(text)
        if file_path:
            if not self.upload_file(file_path):
                return None
        if pin:
            self.set_pin(pin)
        self.set_ttl(ttl)
        self.set_duration_by_value(duration)
        if not self.is_submit_enabled():
            return None
        self.click_submit()
        link = self.get_link_text()
        return link if link else None
            






    
    


    