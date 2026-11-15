# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`comet-sdkp` is a Python wrapper around the CDP4-COMET **.NET** SDK, loaded through `pythonnet`. The whole SDK is one module, `src/comet_sdkp/CDP4Adaptor.py`; the .NET assemblies it wraps are committed as binaries in `src/comet_sdkp/libs/` and shipped in the wheel as package data.

Requires Python 3.12+. Using the SDK for real (not the tests) also needs a .NET runtime that pythonnet can load: .NET Framework on Windows, Mono on Linux/macOS.

## Commands

```bash
pip install -e ".[dev]"        # tests + black, isort, mypy, pylint, build, twine
pip install -e ".[docs]"       # sphinx toolchain

pytest                                        # all tests
pytest tests/unit/test_CDP4Adaptor.py         # one file
pytest tests/unit/test_CDP4Adaptor.py::TestCdp4SessionServiceOpen::test_open_with_valid_parameters
pytest --cov=comet_sdkp --cov-report=term-missing

black src/ tests/ examples/ --check
isort src/ tests/ examples/ --check-only
mypy src/comet_sdkp/ --show-error-codes --pretty
pylint src/comet_sdkp/ --rcfile=pyproject.toml

python -m build                # wheel + sdist into dist/
cd docs && make html           # make.bat html on Windows; output in docs/_build/html
```

Line length is 100 (black, isort, pylint).

## Architecture

### Import-time .NET loading

Importing `comet_sdkp.CDP4Adaptor` does real work: it puts `libs/` on `sys.path`, calls `clr.AddReference("CDP4ServicesDal")`, and then imports .NET namespaces (`System`, `CDP4Common.*`, `CDP4Dal.*`, `CDP4ServicesDal`) as if they were Python modules. A missing or mismatched DLL therefore shows up as an `ImportError` on import, not at call time. `src/comet_sdkp/__init__.py` is empty, so `import comet_sdkp` alone loads nothing and callers import from `comet_sdkp.CDP4Adaptor` directly.

The DLLs in `libs/` are a closed set of transitive dependencies of `CDP4ServicesDal`. They are updated together by hand (see commit `353893d`, which added the ones Mono needs); there is no script that fetches them.

### API shape

- `Cdp4SessionService` owns a `CDP4Dal.Session` and exposes `open`, `close`, `getParticipantModels`, `getAvailableDomains`, `openActiveIteration`, `write`. The .NET async calls are blocked on with `.GetAwaiter().GetResult()`, so the Python API is synchronous.
- Module-level functions operate on the .NET objects the service returns: `computeProductTree`, `getElementByParameterType`, `getElementByParameterTypeWhereAllValuesAreSet`, `prepareTransaction`, `setValue`.
- The write flow is: `openActiveIteration` → `prepareTransaction(iteration)` gives `(clone, ThingTransaction)` → mutate value sets with `setValue` → `service.write(transaction)`.
- Public names are camelCase to mirror the .NET SDK; private helpers are snake_case. Returned objects are raw .NET objects (`.Name`, `.Iid`, `.Option`, ...), not Python wrappers.

### Error-handling convention

This is inconsistent by design and callers (and the README examples) depend on it, so keep it when adding methods:

- Invalid arguments raise `InvalidParametersException`; opening an already-open session or writing without a session raises `SessionException`. Both derive from `Cdp4Exception`.
- Failures of the underlying .NET call do **not** raise. `open`, `close` and `write` return `None` on success and the error message as a `str` on failure. `openActiveIteration` returns the `Iteration` or an error `str`. The list-returning methods and functions log the error and return `[]`.
- `prepareTransaction` and `setValue` are the exceptions: they re-raise (`setValue` wraps unexpected errors in `InvalidParametersException`).

## Tests

No test touches .NET or a server. Each test module replaces `clr`, `System*` and `CDP4*` in `sys.modules` with `MagicMock` *before* importing `comet_sdkp.CDP4Adaptor`, and `tests/conftest.py` does the same in a session fixture. Consequences:

- Every .NET type inside the module under test is a `MagicMock`, so tests can only check the wrapper's own control flow. Anything that depends on real pythonnet behaviour (enum handling in `setValue`, `IEnumerable` conversion, `Predicate[...]`) is not covered and has to be checked against a real server with `examples/script.py`.
- A new .NET namespace imported in `CDP4Adaptor.py` must be added to the mock lists in both test modules and `conftest.py`, or the tests fail at import.
- `tests/integration/` is also fully mocked. The only tests meant for a live server at `http://localhost:5000` are in `TestRealServerIntegration`, and they are disabled by a hard-coded `skipif` that has to be edited to run them.

Configuration traps:

- `pytest.ini` takes precedence, so the `[tool.pytest.ini_options]` block in `pyproject.toml` (coverage `addopts`, `--strict-markers`) is ignored. Coverage only runs when `--cov` is passed.
- `conftest.py` auto-marks tests by looking for `unit` / `integration` / `smoke` as a substring of the test's full path. The repository directory name contains "Comm**unit**y", so in a default clone every test gets the `unit` marker and the other two branches never fire. Select by directory (`pytest tests/unit`) rather than by `-m`.

## Known stale references

- `test_output.txt` is a committed test run from another machine, not a fixture.
- The README and `docs/contributing.md` mention `docs/guides/examples.md`, `docs/architecture/overview.md`, `setup.py`, `CHANGELOG.md` and a GitHub Actions pipeline; none of these exist in the repository.
- The module docstring of `CDP4Adaptor.py` says it wraps a "C++" SDK; the SDK is .NET.
