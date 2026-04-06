import pytest
from typing import Iterator
from utils.data_generator import FakerGenerator

@pytest.fixture
def test_data() -> FakerGenerator:
    return FakerGenerator()


@pytest.fixture
def random_text(test_data) -> str:
    return test_data.text()


@pytest.fixture
def random_pin(test_data) -> str:
    return test_data.pin(6)


@pytest.fixture
def temp_txt_file(test_data) -> Iterator[str]:
    file_path = test_data.temp_txt_file()
    yield file_path
    test_data.cleanup_files(file_path)




