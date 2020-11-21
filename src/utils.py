import time
import random
import os
from pathlib import Path


def project_root() -> Path:
    """return project dir path"""
    return Path(
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..')
        )
    )


def static_path() -> Path:
    """

    :return: Path object with data location
    """
    return Path(os.getenv('API_DATA_DIR', "data"))


def base_url() -> Path:
    """

    :return: Path object with base url
    """
    base = os.getenv('API_BASE_URL', "http://localhost")
    port = os.getenv('API_PORT', "8081")
    return Path(f"{base}:{port}")


def get_random_filename(with_subdirs: bool = False, interval: int = 10000) -> str:
    """
    Return random filename
    :param with_subdirs:
    :param interval:
    :return: filename str with subdirs (or not) with interval in seconds for every new dir
    """
    if with_subdirs:
        t = time.time()
        dirname = int((t - t % interval) / interval)
        filename = f"{t % interval}_{random.randint(1000000, 9000000)}"
        return f"{dirname}/{filename}"
    else:
        return f"{time.time()}_{random.randint(1000000, 9000000)}"
