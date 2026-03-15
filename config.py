import os


class Config:

    #BASIC SETTINGS
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")
    API_BASE_URL = os.getenv("API_BASE_URL", BASE_URL)

    #TIMEOUTS
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))
    POLL_FREQUENCY = float(os.getenv("POLL_FREQUENCY", "1"))
    
    #BROWSER SETTINGS
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    BROWSER_WIDTH = int(os.getenv("BROWSER_WIDTH", "1920"))
    BROWSER_HEIGHT = int(os.getenv("BROWSER_HEIGHT", "1080"))


    
    @classmethod
    def get_api_url(cls) -> str:
        return cls.API_BASE_URL
    
    @classmethod
    def get_ui_url(cls) -> str:
        return cls.BASE_URL