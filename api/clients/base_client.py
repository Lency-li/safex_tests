import requests
import logging
from typing import Dict, Any
from config import Config
from utils.logger import setup_logger


class BaseClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'API-Tests/1.0',
            'Accept': 'application/json, text/html, */*',
        })
        self.logger = setup_logger(
            self.__class__.__name__,
            level=getattr(logging, Config.LOG_LEVEL, logging.INFO)
        )

    def _log_request(self, method: str, url: str, **kwargs):
        self.logger.debug(f"Request: {method} {url}")
        if 'json' in kwargs and kwargs['json'] is not None:
            self.logger.debug(f"Request body (json): {kwargs['json']}")
        if 'data' in kwargs and kwargs['data'] is not None:
            self.logger.debug(f"Request body (data): {kwargs['data']}")
        if 'files' in kwargs:
            file_names = {k: v[0] for k, v in kwargs['files'].items() if isinstance(v, tuple)}
            self.logger.debug(f"Request files: {file_names}")

    def _log_response(self, response: requests.Response):
        self.logger.debug(f"Response status: {response.status_code}")
        content_type = response.headers.get('content-type', '')
        if 'application/json' in content_type or 'text/html' in content_type:
            self.logger.debug(f"Response body: {response.text[:1000]}")
        else:
            self.logger.debug(f"Response body (binary) length: {len(response.content)} bytes")
        if response.status_code >= 400:
            self.logger.error(f"Unexpected status {response.status_code} for {response.url}")

    def _build_url(self, path: str) -> str:
        path = path.lstrip('/')
        return f"{self.base_url}/{path}"
    
    def get(self, path: str, **kwargs) -> requests.Response:
        url = self._build_url(path)
        self._log_request("GET", url, **kwargs)
        response = self.session.get(url, **kwargs)
        self._log_response(response)
        return response
    
    def post(self, path: str, **kwargs) -> requests.Response:
        url = self._build_url(path)
        self._log_request("POST", url, **kwargs)
        response = self.session.post(url, **kwargs)
        self._log_response(response)
        return response
    
    def post_json(self, path: str, data: Dict[str, Any], **kwargs) -> requests.Response:
        kwargs.setdefault('json', data)
        return self.post(path, **kwargs)
    
    def post_multipart(self, path: str, files: Dict[str, tuple], **kwargs) -> requests.Response:
        return self.post(path, files=files, **kwargs)
    
    def close(self) -> None:
        self.session.close()