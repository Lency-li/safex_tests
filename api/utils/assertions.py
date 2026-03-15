import requests
from typing import Optional
from ..models.secret import Secret
from ..models.enums import HTTPStatus


def assert_status_code(
    response: requests.Response,
    expected: int,
    message: Optional[str] = None
):
    if response.status_code != expected:
        error_msg = message or (
            f"Expected {expected}, got {response.status_code}\n"
            f"URL: {response.url}"
        )
        raise AssertionError(error_msg)


def assert_secret_created(
    response: requests.Response,
    expected_secret_id: Optional[str] = None
) -> Secret:
    assert_status_code(response, HTTPStatus.CREATED.value)
    
    try:
        secret = Secret.from_response(response)
    except Exception as e:
        raise AssertionError(f"Failed to parse secret: {e}")
    
    if expected_secret_id and secret.secret_id != expected_secret_id:
        raise AssertionError(
            f"Secret ID mismatch: {secret.secret_id} != {expected_secret_id}"
        )
    
    return secret


def assert_error_response(
    response: requests.Response,
    expected_status: int = HTTPStatus.BAD_REQUEST.value
):
    assert_status_code(response, expected_status)