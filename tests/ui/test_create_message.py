import pytest
from pages.create_message_page import CreateMessagePage
from pages.view_message_page import ViewMessagePage
import allure


@allure.feature("UI tests")
@allure.story("Creating a message")
class TestCreateMessage:
    @pytest.fixture(autouse=True)
    def setup(self, browser, test_data):
        self.create_page = CreateMessagePage(browser)
        self.view_page = ViewMessagePage(browser)
        self.create_page.open()
        self.generator = test_data


    @allure.title("Page Loading")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_page_loaded_successfully(self):
        assert self.create_page.is_text_area_visible(), "The text field is not displayed"
        assert self.create_page.is_pin_input_visible(), "The PIN field is not displayed"
        assert self.create_page.is_file_zone_enabled(), "The file upload area is not active"
        assert self.create_page.is_submit_enabled(), "The send button is not active"
        file_label = self.create_page.find(self.create_page.locators.FILE_LABEL)
        assert file_label.is_displayed(), "The file upload zone is not displayed"


    @allure.title("Creating and viewing a text message")
    @allure.severity(allure.severity_level.CRITICAL)    
    def test_create_and_view_text_message(self, random_text, random_pin):
        link = self.create_page.create_message(text=random_text, pin=random_pin)
        assert link, "The link was not generated"
        print(f'Link: {link}')
        
        self.view_page.open_secret(link, random_pin)
        
        assert self.view_page.has_text(), "The text is not displayed"
        assert self.view_page.verify_text(random_text), "The text of the message does not match"


    @allure.title("Creating and viewing a message with a file")
    @allure.severity(allure.severity_level.CRITICAL)   
    def test_create_and_view_file_message(self, temp_txt_file, random_pin):
        link = self.create_page.create_message(file_path=temp_txt_file, pin=random_pin)
        assert link, "The link was not generated"
        print(f'Link: {link}')
        
        self.view_page.open_secret(link, random_pin)
        
        assert self.view_page.has_file(), "The file is not displayed"

    



    
    
    
    