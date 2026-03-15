import pytest
from api.models import SecretRequestBuilder
from api.utils.assertions import assert_error_response
from utils.data_generator import generator
import allure


@allure.feature("Creating Secrets")
@allure.story("Positive scenarios")
class TestCreateSecret:
    @allure.title("Creating a text secret")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_text_secret_success(self, secret_client, test_secret_data, api_base_url):
        with allure.step("Creating a secret"):
            secret = secret_client.create_secret_success(
                secret_id=test_secret_data["secret_id"],
                opaque_upload=test_secret_data["opaque_upload"]
            )
            
        with allure.step("Checking the result"):
            assert secret.secret_id == test_secret_data["secret_id"]
            assert secret.link.startswith(f"{api_base_url}/secrets/")
            allure.attach(
                secret.link,
                name="Link to the secret",
                attachment_type=allure.attachment_type.TEXT
            )
    
    def test_create_secret_with_builder(self, secret_client, test_secret_data):
        request = (SecretRequestBuilder()
                  .with_ttl(30, "minutes")
                  .as_text()
                  .with_pin(generator.pin(6))
                  .build())
        
        secret = secret_client.create_secret_success(
            secret_id=test_secret_data["secret_id"],
            opaque_upload=test_secret_data["opaque_upload"],
            secret_request=request
        )
        
        assert secret.secret_id == test_secret_data["secret_id"]
    
    def test_create_file_secret_success(self, secret_client, test_secret_data):
        file_content = generator.file_content_for_api(size=2048)
        
        request = (SecretRequestBuilder()
                  .as_file(content=file_content)
                  .build())
        
        secret = secret_client.create_secret_success(
            secret_id=test_secret_data["secret_id"],
            opaque_upload=test_secret_data["opaque_upload"],
            secret_request=request
        )
        
        assert secret.secret_id == test_secret_data["secret_id"]
    
    @pytest.mark.parametrize("ttl,unit", [
        (1, "minutes"),
        (5, "minutes"),
        (1, "hours"),
        (24, "hours"),
    ])
    def test_create_secret_with_different_ttl(self, secret_client, test_secret_data, ttl, unit):
        request = (SecretRequestBuilder()
                  .with_ttl(ttl, unit)
                  .as_text()
                  .build())
        
        secret = secret_client.create_secret_success(
            secret_id=test_secret_data["secret_id"],
            opaque_upload=test_secret_data["opaque_upload"],
            secret_request=request
        )
        
        assert secret.secret_id == test_secret_data["secret_id"]
    
    def test_create_secret_with_pin(self, secret_client, test_secret_data):
        pin = generator.pin(6)
        
        request = (SecretRequestBuilder()
                  .as_text()
                  .with_pin(pin)
                  .build())
        
        secret = secret_client.create_secret_success(
            secret_id=test_secret_data["secret_id"],
            opaque_upload=test_secret_data["opaque_upload"],
            secret_request=request
        )
        
        assert secret.secret_id == test_secret_data["secret_id"]
    
    def test_create_secret_without_required_fields(self, secret_client):
        response = secret_client.create_secret(
            secret_id="",
            opaque_upload=""
        )
        
        assert_error_response(response, 400)
        assert "SecretID is required" in response.text
    
    def test_create_secret_with_invalid_ttl(self, secret_client, test_secret_data):
        invalid_ttls = [0, -5, 10**7]
        
        for ttl in invalid_ttls:
            request = SecretRequestBuilder().with_ttl(ttl, "minutes").build()
            
            response = secret_client.create_secret(
                secret_id=test_secret_data["secret_id"],
                opaque_upload=test_secret_data["opaque_upload"],
                secret_request=request
            )
            
            assert response.status_code in [400, 201]
