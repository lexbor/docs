import os
import socket
import subprocess
import time

import pytest


def _wait_for_port(port: int, timeout: float = 10.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.5):
                return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError(f"Port {port} did not open within {timeout}s")


@pytest.fixture(scope="session")
def docs_server():
    docs_dir = os.path.join(os.path.dirname(__file__), "..", "build")
    docs_dir = os.path.abspath(docs_dir)
    proc = subprocess.Popen(
        ["python3", "-m", "http.server", "--bind", "127.0.0.1", "8000", "--directory", docs_dir],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    _wait_for_port(8000)
    yield "http://127.0.0.1:8000"
    proc.terminate()
    proc.wait()


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {**browser_type_launch_args, "args": ["--no-sandbox", "--disable-dev-shm-usage"]}
