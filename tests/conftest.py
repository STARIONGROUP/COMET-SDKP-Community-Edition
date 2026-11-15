"""
Pytest configuration and fixtures for COMET SDK tests.

This module provides:
- Session-scoped mocks for CDP4 and pythonnet modules
- Test fixtures for common test objects
- Environment setup and cleanup
"""

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

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


# The markers themselves are registered in pyproject.toml ([tool.pytest.ini_options]).
_TESTS_DIR = Path(__file__).parent
_DIRECTORY_MARKERS = ("unit", "integration", "smoke", "live")


def pytest_collection_modifyitems(config, items):
    """
    Modify test collection to add markers based on test location.

    A test gets the marker named after the directory it lives in directly under ``tests/``.
    The directory is taken from the path relative to ``tests/``, so that the location of the
    repository on disk has no influence on the markers.

    Args:
        config: pytest config object
        items: list of collected test items
    """
    for item in items:
        try:
            relative_parts = Path(str(item.fspath)).relative_to(_TESTS_DIR).parts
        except ValueError:
            continue

        if len(relative_parts) > 1 and relative_parts[0] in _DIRECTORY_MARKERS:
            item.add_marker(getattr(pytest.mark, relative_parts[0]))


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
