import time
from typing import Callable


def wait_for_condition(
    condition_func: Callable[[], bool],
    timeout: int = 10,
    interval: float = 0.5,
    error_message: str = "Condition not met"
) -> bool:
    start_time = time.time()
    last_error = None
    
    while time.time() - start_time < timeout:
        try:
            if condition_func():
                return True
        except Exception as e:
            last_error = e
        
        time.sleep(interval)
    
    raise TimeoutError(f"{error_message} after {timeout}s. Last error: {last_error}")


def extract_secret_id_from_link(link: str) -> str:
    return link.split('/')[-1]
