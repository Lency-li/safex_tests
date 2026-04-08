import requests
from typing import Dict, Any


class BaseClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'API-Tests/1.0',
            'Accept': 'application/json, text/html, */*',
        })
    
    def _build_url(self, path: str) -> str:
        path = path.lstrip('/')
        return f"{self.base_url}/{path}"
    
    def _handle_response(self, response: requests.Response) -> requests.Response:
        return response
    
    def get(self, path: str, **kwargs) -> requests.Response:
        url = self._build_url(path)
        return self._handle_response(self.session.get(url, **kwargs))
    
    def post(self, path: str, **kwargs) -> requests.Response:
        url = self._build_url(path)
        return self._handle_response(self.session.post(url, **kwargs))
    
    def post_json(self, path: str, data: Dict[str, Any], **kwargs) -> requests.Response:
        kwargs.setdefault('json', data)
        return self.post(path, **kwargs)
    
    def post_multipart(self, path: str, files: Dict[str, tuple], **kwargs) -> requests.Response:
        return self.post(path, files=files, **kwargs)
    
    def close(self) -> None:
        self.session.close()