"""
Pytest configuration and fixtures for COMET SDK tests.

This module provides:
- Session-scoped mocks for CDP4 and pythonnet modules
- Test fixtures for common test objects
- Environment setup and cleanup
"""

import os
import sys
import pytest
from unittest.mock import MagicMock


###################################################################################################
#                                   SESSION-SCOPED FIXTURES                                      #
###################################################################################################


@pytest.fixture(scope="session", autouse=True)
def mock_cdp4_modules():
    """
    Mock CDP4 and pythonnet modules for the entire test session.

    This fixture must run before any imports of comet_sdkp modules to prevent
    ImportError from missing .NET dependencies.

    This is automatically used in all tests (autouse=True).

    Returns:
        dict: Dictionary of mocked modules
    """
    mocked_modules = {
        # pythonnet
        "clr": MagicMock(),
        # System modules
        "System": MagicMock(),
        "System.Threading": MagicMock(),
        "System.Collections": MagicMock(),
        "System.Collections.Generic": MagicMock(),
        # CDP4 Common modules
        "CDP4Common": MagicMock(),
        "CDP4Common.Helpers": MagicMock(),
        "CDP4Common.EngineeringModelData": MagicMock(),
        "CDP4Common.SiteDirectoryData": MagicMock(),
        "CDP4Common.Types": MagicMock(),
        # CDP4 DAL modules
        "CDP4Dal": MagicMock(),
        "CDP4Dal.DAL": MagicMock(),
        "CDP4Dal.Operations": MagicMock(),
        # CDP4 Services
        "CDP4ServicesDal": MagicMock(),
    }

    # Add all mocks to sys.modules
    for module_name, mock_module in mocked_modules.items():
        sys.modules[module_name] = mock_module

    yield mocked_modules

    # Cleanup: Remove mocked modules after session
    for module_name in mocked_modules.keys():
        sys.modules.pop(module_name, None)


@pytest.fixture(scope="session")
def test_native_path():
    """
    Provides a path to native test libraries if available.

    Returns:
        str or None: Path to native libraries from environment variable
                     or None if not set.

    Note:
        Set the COMET_SDK_NATIVE_PATH environment variable to specify
        the location of native CDP4 libraries.
    """
    return os.environ.get("COMET_SDK_NATIVE_PATH")


###################################################################################################
#                                   FUNCTION-SCOPED FIXTURES                                     #
###################################################################################################


@pytest.fixture
def clean_env(monkeypatch):
    """
    Ensures a clean environment for each test by removing test-related
    environment variables.

    Args:
        monkeypatch: pytest's monkeypatch fixture for modifying environment

    Yields:
        None

    Note:
        This fixture clears the COMET_SDK_NATIVE_PATH variable for each test
        to ensure tests don't interfere with each other through environment state.
    """
    monkeypatch.delenv("COMET_SDK_NATIVE_PATH", raising=False)
    yield
    # Cleanup is automatic when using monkeypatch


###################################################################################################
#                                    PYTEST CONFIGURATION                                        #
###################################################################################################


def pytest_configure(config):
    """
    Configure pytest with custom markers and settings.

    Args:
        config: pytest config object
    """
    config.addinivalue_line("markers", "unit: mark test as a unit test (no external dependencies)")
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test (may require external resources)"
    )
    config.addinivalue_line(
        "markers", "smoke: mark test as a smoke test (basic functionality checks)"
    )
    config.addinivalue_line("markers", "slow: mark test as slow (takes longer to execute)")
    config.addinivalue_line("markers", "skip_ci: mark test to skip in CI/CD pipelines")


def pytest_collection_modifyitems(config, items):
    """
    Modify test collection to add markers based on test location.

    Args:
        config: pytest config object
        items: list of collected test items
    """
    for item in items:
        # Auto-mark tests in specific directories
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "smoke" in str(item.fspath):
            item.add_marker(pytest.mark.smoke)


###################################################################################################
#                                    HELPER FUNCTIONS                                            #
###################################################################################################


def pytest_runtest_logreport(report):
    """
    Log test results for debugging and reporting.

    Args:
        report: test report object
    """
    if report.when == "call":
        if report.outcome == "failed":
            # Log failed tests for CI/CD integration
            pass
        elif report.outcome == "passed":
            # Log passed tests
            pass
