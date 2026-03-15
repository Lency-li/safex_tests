import pytest
from api.clients import OpaqueClient, SecretClient
from config import Config


@pytest.fixture(scope="session")
def api_base_url():
    return Config.get_api_url()


@pytest.fixture(scope="session")
def test_secret_data(api_base_url):
    client = OpaqueClient(api_base_url)
    secret_id, opaque_upload = client.register_start()
    client.close()
    
    return {
        "secret_id": secret_id,
        "opaque_upload": opaque_upload
    }

@pytest.fixture
def opaque_client(api_base_url):
    client = OpaqueClient(api_base_url)
    yield client
    client.close()


@pytest.fixture
def secret_client(api_base_url):
    client = SecretClient(api_base_url)
    yield client
    client.close()