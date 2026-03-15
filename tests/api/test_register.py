from api.models.enums import HTTPStatus
from api.utils.assertions import assert_status_code
import allure 


@allure.feature("Registration")
@allure.story("OPAQUE protocol")
def test_register_success(opaque_client):
    secret_id, response_data = opaque_client.register_start()
    
    assert secret_id is not None
    assert response_data is not None
    assert len(secret_id) == 36 
    assert len(response_data) > 0


def test_register_without_request_fails(opaque_client):
    response = opaque_client.register_start_expecting_error({})
    assert_status_code(response, HTTPStatus.BAD_REQUEST.value)
    assert "Request is required" in response.text


def test_register_with_invalid_request_format(opaque_client):
    invalid_requests = [
        {"request": 12345},
        {"request": ""},      
        {"request": "abc"},   
        {"wrong_field": "data"},  
    ]
    
    for payload in invalid_requests:
        response = opaque_client.register_start_expecting_error(payload)
        assert_status_code(response, HTTPStatus.BAD_REQUEST.value)


def test_register_rate_limit_headers(opaque_client):
    secret_id, _ = opaque_client.register_start()
    
    response = opaque_client.post_json("/opaque/register/start", 
                                       {"request": opaque_client.DEFAULT_REQUEST})
    
    headers = response.headers
    assert "x-ratelimit-limit" in headers
    assert "x-ratelimit-remaining" in headers
    
    limit = int(headers.get("x-ratelimit-limit", 0))
    remaining = int(headers.get("x-ratelimit-remaining", 0))
    
    assert limit > 0
    assert 0 <= remaining <= limit