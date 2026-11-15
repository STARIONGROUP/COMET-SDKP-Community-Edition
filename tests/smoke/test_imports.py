def test_sdk_imports():
    """
    Smoke test: SDK must be importable.
    """
    import comet_sdkp  # noqa: F401


def test_client_import():
    from comet_sdkp.CDP4Adaptor import Cdp4SessionService  # noqa: F401
    from comet_sdkp.CDP4Adaptor import (
        computeProductTree,
        getElementByParameterType,
        getElementByParameterTypeWhereAllValuesAreSet,
        prepareTransaction,
        setValue,
    )
