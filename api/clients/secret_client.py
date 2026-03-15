import requests
from typing import Optional
from .base_client import BaseClient
from ..models.secret import Secret
from ..models.request import SecretRequest
from ..models.enums import HTTPStatus


class SecretClient(BaseClient):
    SECRETS_ENDPOINT = "/secrets"
    
    def create_secret(
        self,
        secret_id: str,
        opaque_upload: str,
        secret_request: Optional[SecretRequest] = None,
        **kwargs
    ) -> requests.Response:
        request = secret_request or SecretRequest()
        files = request.to_multipart()
        files['secret_id'] = (None, secret_id)
        files['opaque_upload'] = (None, opaque_upload)
        
        return self.post_multipart(self.SECRETS_ENDPOINT, files, **kwargs)
    
    def create_secret_success(
        self,
        secret_id: str,
        opaque_upload: str,
        secret_request: Optional[SecretRequest] = None,
        **kwargs
    ) -> Secret:
        response = self.create_secret(secret_id, opaque_upload, secret_request, **kwargs)
        
        if response.status_code != HTTPStatus.CREATED.value:
            raise AssertionError(
                f"Expected 201, got {response.status_code}: {response.text[:200]}"
            )
        
        return Secret.from_response(response, self.base_url)
    
    def get_secret(self, secret_id: str) -> requests.Response:
        return self.get(f"{self.SECRETS_ENDPOINT}/{secret_id}")
    
    def get_secret_success(self, secret_id: str) -> requests.Response:
        response = self.get_secret(secret_id)
        
        if response.status_code != HTTPStatus.OK.value:
            raise AssertionError(
                f"Expected 200, got {response.status_code}"
            )
        
        return response