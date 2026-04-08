import pytest
from api.models import SecretRequestBuilder
from api.models.enums import HTTPStatus
from api.utils.assertions import assert_error_response
import allure



@allure.feature("Creating Secrets")
@allure.story("Negative scenarios")
class TestNegativeScenarios:
    @allure.title("Creating with an invalid secret_id")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("invalid_id", [
    "not-a-uuid",
    "12345",
    "00000000-0000-0000-0000-00000000000Z",
    "",
    " " * 36,
    ])
    def test_create_secret_with_invalid_secret_id(self, secret_client, invalid_id):
        response = secret_client.create_secret(
            secret_id=invalid_id,
            opaque_upload="some-upload-data"
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST.value
    
    def test_create_secret_with_invalid_ttl_unit(self, secret_client, test_secret_data):
        invalid_units = ["year", "decade", "lightyear", "", "123", "MINUTES"]
        
        for unit in invalid_units:
            files = {
                'ttl': (None, '15'),
                'ttl_unit': (None, unit),
                'secret_id': (None, test_secret_data["secret_id"]),
                'opaque_upload': (None, test_secret_data["opaque_upload"]),
                'file': ('file.bin', b'test', 'application/octet-stream'),
                'payload_type': (None, 'text'),
            }
            
            response = secret_client.post_multipart("/secrets", files)
            
            assert response.status_code in [400, 201]
    
    def test_create_secret_with_huge_payload(self, secret_client, test_secret_data, test_data):
        huge_content = test_data.file_content_for_api(size=10 * 1024 * 1024)
        
        request = SecretRequestBuilder().as_file(content=huge_content).build()
        
        response = secret_client.create_secret(
            secret_id=test_secret_data["secret_id"],
            opaque_upload=test_secret_data["opaque_upload"],
            secret_request=request
        )
        
        assert response.status_code in [201, 413]
    
    def test_malformed_json_in_register(self, opaque_client, test_data):
        random_string = test_data.text()
        response = opaque_client.session.post(
            f"{opaque_client.base_url}/opaque/register/start",
            data=random_string
        )
        assert_error_response(response, 400)
    
    def test_wrong_http_method(self, secret_client):
        response = secret_client.get("/secrets")
        assert response.status_code in [404, 405, 400]
        
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = secret_client.post(f"/secrets/{fake_id}")
        assert response.status_code in [404, 405, 400]
    

    @pytest.mark.parametrize("ttl", [0, -5, 10**7])
    def test_create_secret_with_invalid_ttl(self, secret_client, test_secret_data, ttl):
        request = SecretRequestBuilder().with_ttl(ttl, "minutes").build()
        response = secret_client.create_secret(
            secret_id=test_secret_data["secret_id"],
            opaque_upload=test_secret_data["opaque_upload"],
            secret_request=request
        )
        assert response.status_code in [400, 201]