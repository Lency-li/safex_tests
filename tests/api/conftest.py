import pytest
from typing import Generator, Dict
from api.clients import OpaqueClient, SecretClient
from config import Config


@pytest.fixture(scope="session")
def api_base_url() -> str:
    return Config.get_api_url()


@pytest.fixture(scope="session")
def test_secret_data(api_base_url: str) -> Dict[str, str]:
    client = OpaqueClient(api_base_url)
    secret_id, opaque_upload = client.register_start()
    client.close()
    
    return {
        "secret_id": secret_id,
        "opaque_upload": opaque_upload
    }

@pytest.fixture
def opaque_client(api_base_url: str) -> Generator[OpaqueClient, None, None]:
    client = OpaqueClient(api_base_url)
    yield client
    client.close()


@pytest.fixture
def secret_client(api_base_url: str) -> Generator[SecretClient, None, None]:
    client = SecretClient(api_base_url)
    yield client
    client.close()