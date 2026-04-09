from typing import Tuple, Optional
from .base_client import BaseClient
import requests
import time

class OpaqueClient(BaseClient):
    REGISTER_START = "/opaque/register/start"
    DEFAULT_REQUEST = "Qjzp+pNdR9kXa+MNZnmxIFlIiEHvlT4hUZYRZ9RRSg4="
    
    def register_start(self, request_data: Optional[str] = None, max_retries: int = 3) -> Tuple[str, str]:
        payload = {"request": request_data or self.DEFAULT_REQUEST}
        
        for attempt in range(max_retries):
            response = self.post_json(self.REGISTER_START, payload)

            if response.status_code == 200:
                data = response.json()
                self.logger.info(f"Register start successful: secretId={data['secretId'][:8]}...")
                return data["secretId"], data["response"]
            
            if response.status_code == 429 and attempt < max_retries - 1:
                wait_time = 2 ** attempt
                self.logger.warning(f"Rate limit (429), retry in {wait_time}s (attempt {attempt+1}/{max_retries})")
                time.sleep(wait_time)
                continue

            self.logger.error(f"Register start failed: {response.status_code} - {response.text}")
            raise Exception(f"Register start failed: {response.status_code} - {response.text}")
        raise Exception(f"Failed after {max_retries} retries due to rate limit")
    
    def register_start_expecting_error(
        self, 
        request_data: Optional[dict] = None,
        expected_status: int = 400
    ) -> requests.Response:
        payload = request_data or {}
        response = self.post_json(self.REGISTER_START, payload)
        
        if response.status_code != expected_status:
            raise AssertionError(
                f"Expected {expected_status}, got {response.status_code}"
            )
        
        return response