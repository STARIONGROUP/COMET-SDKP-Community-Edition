import os
import pytest
 
 
@pytest.fixture(scope="session")
def test_native_path():
    """
    Provides a path to native test libraries if available.
    """
    return os.environ.get("COMET_SDK_NATIVE_PATH")
 
 
@pytest.fixture
def clean_env(monkeypatch):
    """
    Ensures a clean environment for each test.
    """
    monkeypatch.delenv("COMET_SDK_NATIVE_PATH", raising=False)