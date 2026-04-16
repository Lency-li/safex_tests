from api.models.enums import HTTPStatus
from api.utils.helpers import extract_secret_id_from_link
import allure


@allure.feature("Getting secrets")
class TestRetrieveSecret:
    @allure.title("Getting an existing secret")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_retrieve_existing_secret(self, secret_client, test_secret_data):
        secret = secret_client.create_secret_success(
            secret_id=test_secret_data["secret_id"],
            opaque_upload=test_secret_data["opaque_upload"]
        )
        
        secret_id = extract_secret_id_from_link(secret.link)
        response = secret_client.get_secret_success(secret_id)
        
        assert response.status_code == HTTPStatus.OK.value
        assert test_secret_data["secret_id"] in response.text
    
    def test_retrieve_nonexistent_secret(self, secret_client):
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = secret_client.get_secret(fake_id)
        
        assert response.status_code == 200
        assert "data-secret-id" not in response.text, "The data-secret-id attribute has been found"
        assert "unlock-pin" in response.text, "There is no PIN input field"
        assert "pin" in response.text.lower(), "There is no mention of PIN"
    
    def test_retrieve_secret_multiple_times(self, secret_client, test_secret_data):
        secret = secret_client.create_secret_success(
            secret_id=test_secret_data["secret_id"],
            opaque_upload=test_secret_data["opaque_upload"]
        )
        
        secret_id = extract_secret_id_from_link(secret.link)
        
        for _ in range(3):
            response = secret_client.get_secret_success(secret_id)
            assert response.status_code == HTTPStatus.OK.value
    