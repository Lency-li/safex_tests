from enum import Enum


class PayloadType(str, Enum):
    TEXT = "text"
    FILE = "file"
    
    def __str__(self):
        return self.value


class TTLUnit(str, Enum):
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"
    
    def __str__(self):
        return self.value
    
    def to_seconds(self, value: int) -> int:
        multipliers = {
            self.MINUTES: 60,
            self.HOURS: 3600,
            self.DAYS: 86400,
        }
        return value * multipliers[self]


class HTTPStatus(Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    TOO_MANY_REQUESTS = 429
    SERVER_ERROR = 500
    
    def is_success(self) -> bool:
        return 200 <= self.value < 300
    
    def is_client_error(self) -> bool:
        return 400 <= self.value < 500
    
    def is_server_error(self) -> bool:
        return 500 <= self.value < 600