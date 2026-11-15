![CDP4-COMET-Logo](https://raw.githubusercontent.com/STARIONGROUP/COMET-WebServices-Community-Edition/master/COMET-Community-Edition.jpg)

# COMET SDKP Community Edition

A Python SDK providing clean, Pythonic bindings to the COMET native SDK (CDP4 - COMET Data Exchange Protocol).

[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue)](https://www.python.org/downloads/)
[![License: LGPL-2.1](https://img.shields.io/badge/License-LGPL--2.1-green.svg)](LICENSE)

## Features

- **Session management** - connect to a CDP4-COMET server, list the models and domains available to the user, open the active iteration
- **Product tree navigation** - compute the nested element tree of an iteration for an option
- **Parameter filtering** - filter elements by parameter type and by whether their values are set
- **Transactions** - prepare a transaction, change parameter values and write them back to the server
- **Type hints** and logging through the standard `logging` module

## Requirements

- Python 3.12 or higher
- [pythonnet](https://pythonnet.github.io/) >= 3.0.5 (installed automatically)
- .NET Framework (for the pythonnet integration)
- Network access to a CDP4-COMET server at runtime

## Installation

Use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**From a wheel file** (recommended):

```bash
pip install comet_sdkp-0.1.0-py3-none-any.whl
```

**From source:**

```bash
git clone https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition.git
cd COMET-SDKP-Community-Edition
pip install .
```

To build the wheel yourself, run `pip install build` and `python -m build`; the wheel is written to `dist/`.

Verify the installation:

```bash
python -c "from comet_sdkp.CDP4Adaptor import Cdp4SessionService; print('SDK installed successfully')"
```

See the [Installation Guide](docs/guides/installation.md) for details.

## Quick Start

```python
from comet_sdkp.CDP4Adaptor import Cdp4SessionService

service = Cdp4SessionService()

# open() returns None on success, an error string on failure
result = service.open("http://localhost:5000", "admin", "password")

if result is None:
    models = service.getParticipantModels()
    print(f"Found {len(models)} models")
    for model in models:
        print(f"  - {model.Name}")

    # Always close the session
    service.close()
else:
    print(f"Failed to connect: {result}")
```

## Usage Example: Read and Modify Parameters

```python
from comet_sdkp.CDP4Adaptor import (
    Cdp4SessionService,
    computeProductTree,
    getElementByParameterTypeWhereAllValuesAreSet,
    prepareTransaction,
    setValue,
    InvalidParametersException,
)
from CDP4Common.EngineeringModelData import ParameterSwitchKind

service = Cdp4SessionService()
result = service.open("http://localhost:5000", "admin", "password")

if result is None:
    try:
        # Open the active iteration of the first model
        model = service.getParticipantModels()[0]
        domains = service.getAvailableDomains(model)
        iteration = service.openActiveIteration(model, domains[0])

        if iteration and iteration.Option:
            # Compute the product tree and find the elements with a Mass parameter
            tree = computeProductTree(iteration, iteration.Option[0])
            mass_elements = getElementByParameterTypeWhereAllValuesAreSet(tree, "Mass")
            print(f"Found {len(mass_elements)} elements with Mass")

            # Prepare a transaction and modify the values
            cloned_iteration, transaction = prepareTransaction(iteration)

            for element in mass_elements:
                for param in element.NestedParameter:
                    if hasattr(param, "ValueSet"):
                        for value_set in param.ValueSet:
                            setValue(value_set, ParameterSwitchKind.MANUAL, ["100.0"])

            # write() returns None on success, an error string on failure
            write_result = service.write(transaction)
            if write_result is None:
                print("Changes written successfully")
            else:
                print(f"Write failed: {write_result}")

    except InvalidParametersException as e:
        print(f"Error: {e}")
    finally:
        service.close()
else:
    print(f"Failed to connect: {result}")
```

A complete script is available in [examples/script.py](examples/script.py).

## Documentation

- [Installation Guide](docs/guides/installation.md)
- [Getting Started Guide](docs/guides/getting_started.md)
- [API Reference](docs/api/comet_sdkp.md)
- [FAQ](docs/guides/faq.md)
- [Troubleshooting](docs/guides/troubleshooting.md)

For the CDP4-COMET data model, types and concepts:

- [COMET Development Documentation](https://comet-dev-docs.mbsehub.org/)
- [COMET SDK Wiki](https://github.com/STARIONGROUP/COMET-SDK-Community-Edition/wiki)
- [CDP4-COMET Repository](https://github.com/STARIONGROUP/CDP4-COMET)

## Development

Install in development mode, which adds the test and code quality tools:

```bash
pip install -e ".[dev]"
```

### Tests

```bash
# All tests
pytest tests/ -v

# One kind of test, by marker: unit, integration, smoke or live
pytest -m unit -v

# A single test
pytest tests/unit/test_CDP4Adaptor.py::TestCdp4SessionServiceOpen::test_open_with_valid_parameters -v
```

Every run reports coverage and writes an HTML report to `coverage_html/`; pass `--no-cov` to switch that off.

The unit, integration and smoke tests mock the .NET libraries and do not need a CDP4-COMET server. The tests in `tests/live/` run against a real server and are skipped unless `COMET_TEST_SERVER_URL`, `COMET_TEST_USERNAME` and `COMET_TEST_PASSWORD` are set; see the [Contributing Guide](docs/contributing.md).

### Code Quality

```bash
black src/ tests/ examples/ --check
isort src/ tests/ examples/ --check-only
mypy src/comet_sdkp/ --show-error-codes --pretty
pylint src/comet_sdkp/ --rcfile=pyproject.toml
```

Run `black` and `isort` without the check flags to apply the formatting.

### Building the Documentation

```bash
pip install -e ".[docs]"
cd docs
make html          # On Windows: make.bat html
```

The output is written to `docs/_build/html/index.html`.

## Contributing

Contributions are welcome; see the [Contributing Guide](docs/contributing.md).

## Support

- **Bug reports**: [GitHub Issues](https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition/issues)
- **Questions**: [GitHub Discussions](https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition/discussions)

## Changelog

### v0.1.0 (January 2026)

Initial public release: session management (`Cdp4SessionService`), product tree navigation (`computeProductTree`), parameter filtering (`getElementByParameterType`, `getElementByParameterTypeWhereAllValuesAreSet`) and transaction support (`prepareTransaction`, `setValue`).

See [GitHub Releases](https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition/releases) for later changes.

## License

The COMET SDKP Community Edition is licensed under the [LGPL-2.1](LICENSE).

## Authors

**STARION GROUP** - [stariongroup.eu](https://www.stariongroup.eu) - [info@stariongroup.eu](mailto:info@stariongroup.eu) - [@STARIONGROUP](https://github.com/STARIONGROUP)
