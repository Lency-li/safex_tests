import pytest
from utils.data_generator import FakerGenerator

@pytest.fixture
def test_data():
    return FakerGenerator()


@pytest.fixture
def random_text(test_data):
    return test_data.text()


@pytest.fixture
def temp_txt_file(test_data):
    file_path = test_data.temp_txt_file()
    yield file_path
    test_data.cleanup(file_path)

@pytest.fixture
def random_pin(test_data):
    return test_data.pin(6)


