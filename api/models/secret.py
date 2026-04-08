from dataclasses import dataclass
from typing import Optional, Dict, Any
import re
from datetime import datetime

@dataclass
class Secret:
    secret_id: str
    link: str
    
    ttl: Optional[int] = None
    ttl_unit: Optional[str] = None
    created_at: Optional[datetime] = None
    payload_type: Optional[str] = None
    
    metadata: Optional[Dict[str, Any]] = None
    
    raw_html: Optional[str] = None
    raw_response: Optional[object] = None
    
    @classmethod
    def from_response(cls, response, base_url: str = None):
        html = response.text
        
        secret_id = cls._extract_secret_id(html)
        link = cls._extract_link(html, base_url)
        
        return cls(
            secret_id=secret_id,
            link=link,
            raw_html=html,
            raw_response=response
        )
    
    @staticmethod
    def _extract_secret_id(html: str) -> str:
        patterns = [
            r'data-secret-id="([a-f0-9-]+)"',     
            r'/secrets/([a-f0-9-]+)',                
            r'data-copy-text="[^"]*/([a-f0-9-]+)"',  
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                return match.group(1)
        
        raise ValueError("Secret ID not found in HTML")
    
    @staticmethod
    def _extract_link(html: str, base_url: str = None) -> str:
        patterns = [
            r'data-copy-text="([^"]+)"',              
            r'(https?://[^/]+/secrets/[a-f0-9-]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                return match.group(1)
        
        secret_id = Secret._extract_secret_id(html)
        
        if base_url:
            return f"{base_url}/secrets/{secret_id}"
        return f"/secrets/{secret_id}"
    
    @property
    def short_id(self) -> str:
        return self.secret_id[:8]
    
    def __str__(self) -> str:
        return f"Secret(id={self.short_id}..., link={self.link})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "secret_id": self.secret_id,
            "link": self.link,
            "ttl": self.ttl,
            "ttl_unit": self.ttl_unit,
            "short_id": self.short_id,
        }