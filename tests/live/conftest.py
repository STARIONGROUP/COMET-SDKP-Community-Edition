"""
Fixtures for the tests that run against a real CDP4-COMET server.

These tests are skipped unless the following environment variables are set:

- COMET_TEST_SERVER_URL: the URL of the server, for example http://localhost:5000
- COMET_TEST_USERNAME: the user to authenticate with
- COMET_TEST_PASSWORD: the password of that user

The other test modules replace ``clr`` and the .NET namespaces in ``sys.modules`` with mocks. The
fixtures below take those mocks away for the duration of a live test module, so that
``comet_sdkp.CDP4Adaptor`` is imported with the real pythonnet and the real CDP4-COMET libraries,
and put them back afterwards.
"""

import importlib
import os
import sys

import pytest

SERVER_URL_VARIABLE = "COMET_TEST_SERVER_URL"
USERNAME_VARIABLE = "COMET_TEST_USERNAME"
PASSWORD_VARIABLE = "COMET_TEST_PASSWORD"

_ADAPTOR_MODULE = "comet_sdkp.CDP4Adaptor"


def _is_dotnet_module(name: str) -> bool:
    """Tells whether a module name is pythonnet or one of the .NET namespaces the SDK imports."""
    root = name.split(".")[0]
    return root in ("clr", "System") or root.startswith("CDP4")


@pytest.fixture(scope="session")
def live_server_settings():
    """
    Provides the connection settings of the server to test against.

    Returns:
        dict: the ``url``, ``username`` and ``password`` to use

    Note:
        Skips the requesting test when one of the environment variables is not set.
    """
    settings = {
        "url": os.environ.get(SERVER_URL_VARIABLE),
        "username": os.environ.get(USERNAME_VARIABLE),
        "password": os.environ.get(PASSWORD_VARIABLE),
    }

    if not all(settings.values()):
        pytest.skip(
            f"Requires a CDP4-COMET server: set {SERVER_URL_VARIABLE}, {USERNAME_VARIABLE} "
            f"and {PASSWORD_VARIABLE} to run the live tests"
        )

    return settings


@pytest.fixture(scope="module")
def adaptor(live_server_settings):
    """
    Provides ``comet_sdkp.CDP4Adaptor`` imported against the real .NET libraries.

    Yields:
        module: the CDP4Adaptor module, without any mocked dependency
    """
    package = importlib.import_module("comet_sdkp")
    missing = object()
    previous_attribute = getattr(package, "CDP4Adaptor", missing)

    # Set the mocked modules aside, together with the adaptor that was imported against them
    set_aside = {
        name: module
        for name, module in list(sys.modules.items())
        if name == _ADAPTOR_MODULE or _is_dotnet_module(name)
    }
    for name in set_aside:
        del sys.modules[name]

    try:
        yield importlib.import_module(_ADAPTOR_MODULE)
    finally:
        # Remove the real modules and put the mocked ones back for the remaining tests
        for name in list(sys.modules):
            if name == _ADAPTOR_MODULE or _is_dotnet_module(name):
                del sys.modules[name]
        sys.modules.update(set_aside)

        if previous_attribute is missing:
            if hasattr(package, "CDP4Adaptor"):
                delattr(package, "CDP4Adaptor")
        else:
            setattr(package, "CDP4Adaptor", previous_attribute)


@pytest.fixture
def live_service(adaptor, live_server_settings):
    """
    Provides a Cdp4SessionService with an open session to the server.

    Yields:
        Cdp4SessionService: the service; the session is closed after the test
    """
    service = adaptor.Cdp4SessionService()
    error = service.open(
        live_server_settings["url"],
        live_server_settings["username"],
        live_server_settings["password"],
    )
    assert error is None, f"Could not open a session: {error}"

    yield service

    if service.isSessionOpen:
        service.close()
