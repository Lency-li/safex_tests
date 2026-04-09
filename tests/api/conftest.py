import pytest
import logging
from typing import Generator, Dict
from api.clients import OpaqueClient, SecretClient
from config import Config


@pytest.fixture(scope="session")
def api_base_url() -> str:
    return Config.get_api_url()


logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def test_secret_data(api_base_url):
    logger.info("Creating test secret data (session-scoped)")
    client = OpaqueClient(api_base_url)
    secret_id, opaque_upload = client.register_start()
    logger.info(f"Test secret created: secret_id={secret_id[:8]}...")
    client.close()
    yield {"secret_id": secret_id, "opaque_upload": opaque_upload}
    logger.info(f"Test secret cleanup (no action needed): {secret_id[:8]}...")

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