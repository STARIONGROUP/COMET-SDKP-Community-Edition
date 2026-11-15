"""
Tests for the CDP4Adaptor module against a real CDP4-COMET server.

Nothing is mocked here: the tests use pythonnet, the .NET libraries and a running server. They are
skipped unless the environment variables described in ``tests/live/conftest.py`` are set.
"""

import pytest


class TestLiveSession:
    """Tests for the session lifecycle against a real server"""

    def test_open_and_close(self, adaptor, live_server_settings):
        """Test that a session can be opened and closed"""
        service = adaptor.Cdp4SessionService()

        result = service.open(
            live_server_settings["url"],
            live_server_settings["username"],
            live_server_settings["password"],
        )

        try:
            assert result is None
            assert service.isSessionOpen is True

            site_directory = service.session.RetrieveSiteDirectory()
            assert site_directory is not None
        finally:
            close_result = service.close()

        assert close_result is None
        assert service.isSessionOpen is False

    def test_open_with_wrong_password_returns_error(self, adaptor, live_server_settings):
        """Test that a failed authentication is reported as an error string"""
        service = adaptor.Cdp4SessionService()

        result = service.open(
            live_server_settings["url"],
            live_server_settings["username"],
            live_server_settings["password"] + "-wrong",
        )

        try:
            assert isinstance(result, str)
            assert service.isSessionOpen is False
        finally:
            if service.isSessionOpen:
                service.close()


class TestLiveModels:
    """Tests for reading models from a real server"""

    def test_get_participant_models(self, live_service):
        """Test that the participant models are returned as a list"""
        models = live_service.getParticipantModels()

        assert isinstance(models, list)

    def test_open_active_iteration(self, live_service):
        """Test opening the active iteration of the first model the user participates in"""
        models = live_service.getParticipantModels()
        if not models:
            pytest.skip("The test user does not participate in any model")

        domains = live_service.getAvailableDomains(models[0])
        if not domains:
            pytest.skip("The test user has no domain of expertise in the first model")

        iteration = live_service.openActiveIteration(models[0], domains[0])

        # openActiveIteration returns an error string on failure
        assert not isinstance(iteration, str), iteration
        assert iteration is not None
