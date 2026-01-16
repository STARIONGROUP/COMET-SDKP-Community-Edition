import pytest
from comet_sdkp.CDP4Adaptor import *

def test_session_instantiation():
    """
        tests instantiation of the Session Service.
    """
    testSession = Cdp4SessionService()
    assert testSession is not None

def test_session_has_expected_methods():
    """
        tests Session Service instance has the expected methods and attributes
    """
    testSession = Cdp4SessionService()
    assert hasattr(testSession, "open")
    assert hasattr(testSession, "getParticipantModels")
    assert hasattr(testSession, "getAvailableDomains")
    assert hasattr(testSession, "openActiveIteration")
    assert hasattr(testSession, "write")
    assert hasattr(testSession, "dal")
    assert hasattr(testSession, "messageBus")
    assert hasattr(testSession, "isSessionOpen")