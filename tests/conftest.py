from typing import Iterator
from utils.data_generator import FakerGenerator
from config import Config
import pytest
import logging


def pytest_configure(config: pytest.Config) -> None:
    Config.LOG_DIR.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, Config.LOG_LEVEL, logging.INFO))

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    console = logging.StreamHandler()
    console.setLevel(getattr(logging, Config.LOG_LEVEL, logging.INFO))
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console.setFormatter(formatter)
    root_logger.addHandler(console)

    file_handler = logging.FileHandler(Config.LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG) 
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)

@pytest.fixture(autouse=True)
def log_test_boundary(request):
    logger = logging.getLogger(__name__)
    test_name = request.node.name
    logger.info(f"STARTED: {test_name}")
    yield
    logger.info(f"FINISHED: {test_name}")

def pytest_runtest_makereport(item, call):
    if call.when == "call" and call.excinfo is not None:
        logger = logging.getLogger(__name__)
        logger.error(f"Test failed: {item.name}")
        logger.error(f"Exception: {call.excinfo}")


@pytest.fixture
def test_data() -> FakerGenerator:
    return FakerGenerator()


@pytest.fixture
def random_text(test_data) -> str:
    return test_data.text()


@pytest.fixture
def random_pin(test_data) -> str:
    return test_data.pin(6)

logger = logging.getLogger(__name__)

@pytest.fixture
def temp_txt_file(test_data) -> Iterator[str]:
    file_path = test_data.temp_txt_file()
    logger.info(f"Temporary file created: {file_path}")
    yield file_path
    test_data.cleanup_files(file_path)
    logger.info(f"Temporary file cleaned up: {file_path}")



