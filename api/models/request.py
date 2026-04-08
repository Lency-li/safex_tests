from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from .enums import PayloadType, TTLUnit


@dataclass
class SecretRequest:
    ttl: int = 15
    ttl_unit: TTLUnit = TTLUnit.MINUTES
    payload_type: PayloadType = PayloadType.TEXT
    file_content: bytes = field(default_factory=lambda: b"Default test content")
    
    pin: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self) -> None:
        self._validate()
    
    def _validate(self) -> None:
        if self.ttl <= 0:
            raise ValueError(f"TTL must be positive, got {self.ttl}")
        
        if self.ttl > 10**6:
            raise ValueError(f"TTL too large: {self.ttl}")
        
        if self.pin and (len(self.pin) < 4 or len(self.pin) > 8):
            raise ValueError(f"PIN must be 4-8 digits, got {len(self.pin)}")
        
        if self.pin and not self.pin.isdigit():
            raise ValueError(f"PIN must contain only digits, got {self.pin}")
    
    def to_multipart(self) -> Dict[str, tuple]:
        files = {
            'ttl': (None, str(self.ttl)),
            'ttl_unit': (None, str(self.ttl_unit)),
            'payload_type': (None, str(self.payload_type)),
        }
        
        if self.pin:
            files['pin'] = (None, self.pin)
        
        files['file'] = (
            'message.encrypted',
            self.file_content,
            'application/octet-stream'
        )
        
        return files
    
    @property
    def ttl_in_seconds(self) -> int:
        return self.ttl_unit.to_seconds(self.ttl)
    
    def __str__(self) -> str:
        pin_str = f", pin={self.pin}" if self.pin else ""
        return f"SecretRequest(ttl={self.ttl} {self.ttl_unit}, type={self.payload_type}{pin_str})"


class SecretRequestBuilder:
    def __init__(self):
        self._request = SecretRequest()
    
    def with_ttl(self, value: int, unit: str = "minutes") -> 'SecretRequestBuilder':
        self._request.ttl = value
        self._request.ttl_unit = TTLUnit(unit)
        return self
    
    def as_text(self) -> 'SecretRequestBuilder':
        self._request.payload_type = PayloadType.TEXT
        self._request.file_content = b"Text content for secret"
        return self
    
    def as_file(self, content: bytes = None) -> 'SecretRequestBuilder':
        self._request.payload_type = PayloadType.FILE
        if content:
            self._request.file_content = content
        return self
    
    def with_pin(self, pin: str) -> 'SecretRequestBuilder':
        self._request.pin = pin
        return self
    
    def build(self) -> SecretRequest:
        return self._request


def default_text_request() -> SecretRequest:
    return SecretRequest()


