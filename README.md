![CDP4-COMET-Logo](https://raw.githubusercontent.com/STARIONGROUP/COMET-WebServices-Community-Edition/master/COMET-Community-Edition.jpg)

# COMET SDKP Community Edition

A Python SDK providing clean, Pythonic bindings to the COMET native SDK (CDP4 - COMET Data Exchange Protocol).

This repository contains the **Community Edition** of the COMET Python SDK, focused on stability, clarity, and open usage without enterprise-specific features.

[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue)](https://www.python.org/downloads/)
[![License: LGPL-2.1](https://img.shields.io/badge/License-LGPL--2.1-green.svg)](LICENSE)
[![Status: Active](https://img.shields.io/badge/Status-Active-brightgreen)]()

---

## 📋 Table of Contents

- [Features](#-features)
- [System Requirements](#-system-requirements)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Documentation](#-documentation)
- [Project Structure](#-project-structure)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)
- [Support](#-support)

---

## ✨ Features

- **Pythonic API** - Clean, intuitive Python interface to CDP4
- **Session Management** - Connect to CDP4 servers and manage sessions
- **Product Tree Navigation** - Compute and traverse nested element hierarchies
- **Parameter Filtering** - Filter elements by parameter types and values
- **Transaction Support** - Prepare and execute transactions for data modifications
- **Domain Support** - Work with multiple domains of expertise
- **Error Handling** - Comprehensive error handling and logging
- **Type Hints** - Full type hint support for IDE autocomplete
- **Modern Packaging** - Built with `pyproject.toml` and modern Python standards
- **Full Documentation** - Sphinx + MyST documentation with examples
- **Automated Testing** - Complete pytest test suite (unit, integration, smoke tests)

---

## 📦 System Requirements

### Python Version
- **Python 3.12 or higher** (required)
- Python 3.11 and earlier are not supported

### Operating System
- Windows (tested on Windows 11)
- macOS (10.14+)
- Linux (Ubuntu 20.04+, Fedora 32+, etc.)

### Other Requirements
- **pythonnet** >= 3.0.5 (automatically installed)
- **.NET Framework** (for pythonnet integration)
- Minimum 512MB RAM
- 100MB disk space for SDK and dependencies
- Network access to a CDP4 server (for runtime functionality)

### Verify Python Version

```bash
python --version
# Output should be: Python 3.12.x or higher
```

If you need to use an older Python version, please open a [GitHub Issue](https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition/issues).

---

## 🚀 Quick Start

### 1. Install from Wheel File

Download the wheel file (`.whl`) and install it:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install from the wheel file
pip install comet_sdkp-0.1.0-py3-none-any.whl
```

### 2. Create Your First Script

```python
from comet_sdkp.CDP4Adaptor import Cdp4SessionService

# Initialize service
service = Cdp4SessionService()

# Connect to CDP4 server
result = service.open("http://localhost:5000", "admin", "password")

# Check if connection was successful (open() returns None on success, error string on failure)
if result is None:
    print("✓ Connected successfully")
    
    # Get available models
    models = service.getParticipantModels()
    print(f"✓ Found {len(models)} models")
    
    # List them
    for model in models:
        print(f"  - {model.Name}")
    
    # Always close the session
    service.close()
else:
    print(f"✗ Failed to connect: {result}")
```

### 3. Run Your Script

```bash
python script.py
```

Expected output:
```
✓ Connected successfully
✓ Found 2 models
  - Satellite System
  - Thermal Model
```

---

## 📥 Installation

### Prerequisites

Ensure you have Python 3.12+ installed:

```bash
python --version
```

### Method 1: Install from Wheel File ⭐ (Recommended)

This is the **preferred and easiest installation method**.

**Get the Wheel File:**
- Download `comet_sdkp-0.1.0-py3-none-any.whl` from your distribution source

**Install:**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install from the wheel file
pip install comet_sdkp-0.1.0-py3-none-any.whl
```

**Verify Installation:**
```bash
python -c "from comet_sdkp.CDP4Adaptor import Cdp4SessionService; print('✓ SDK installed successfully')"
```

### Method 2: Clone and Install from Source

For development, contributions, or if you don't have the wheel file:

```bash
# Clone the repository
git clone https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition.git
cd COMET-SDKP-Community-Edition

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install from source
pip install .
```

### Method 3: Development Installation ⭐ (For Contributors)

If you want to contribute or modify the code:

```bash
# Clone the repository
git clone https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition.git
cd COMET-SDKP-Community-Edition

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install in development mode with all tools
pip install -e ".[dev]"
```

Benefits of development mode:
- Code changes take effect immediately
- Access to testing tools (pytest, pytest-cov, pytest-mock)
- Access to code quality tools (black, isort, mypy, pylint)
- Can build documentation locally
- Can contribute to the project

### Method 4: Build Wheel File Locally

If you want to build a wheel file from source:

```bash
# Clone the repository
git clone https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition.git
cd COMET-SDKP-Community-Edition

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install build tools
pip install build

# Build the distribution
python -m build

# The wheel file will be in dist/
# Install from it
pip install dist/comet_sdkp-0.1.0-py3-none-any.whl
```

### Optional Dependencies

If you installed from wheel and need additional features:

```bash
# Testing tools
pip install pytest pytest-cov pytest-mock

# Code quality tools
pip install black isort mypy pylint

# Documentation tools (to build docs locally)
pip install sphinx myst-parser pydata-sphinx-theme sphinx-autodoc-typehints

# All development tools (from source installation)
pip install -e ".[dev]"
```

---

## 📚 Documentation

Full documentation is available in the `docs/` directory or [built locally](#build-documentation-locally).

### SDK Documentation

- **[Installation Guide](docs/guides/installation.md)** - Detailed installation instructions
- **[Getting Started Guide](docs/guides/getting_started.md)** - Step-by-step tutorial
- **[Examples](docs/guides/examples.md)** - Practical code examples
- **[API Reference](docs/api/comet_sdkp.md)** - Complete API documentation
- **[FAQ](docs/guides/faq.md)** - Frequently asked questions
- **[Troubleshooting](docs/guides/troubleshooting.md)** - Solutions to common issues
- **[Architecture Overview](docs/architecture/overview.md)** - System design and architecture

### CDP4-COMET Data Model Documentation

For information about the CDP4-COMET data model, types, and concepts:

- 📖 **[COMET Development Documentation](https://comet-dev-docs.mbsehub.org/)** - Official COMET documentation
- 🔗 **[COMET SDK Wiki](https://github.com/STARIONGROUP/COMET-SDK-Community-Edition/wiki)** - SDK and integration guide
- 🐙 **[CDP4-COMET Repository](https://github.com/STARIONGROUP/CDP4-COMET)** - Main COMET platform source code

### Build Documentation Locally

If you installed from source with documentation tools:

```bash
# Install documentation dependencies (if not already installed)
pip install -e ".[docs]"

# Build HTML
cd docs
make html          # On Linux/macOS
# OR
make.bat html      # On Windows

# View in browser
start _build/html/index.html      # Windows
open _build/html/index.html       # macOS
xdg-open _build/html/index.html   # Linux

# Or serve locally
python -m http.server -d _build/html 8000
# Then visit http://localhost:8000
```

---

## 📁 Project Structure

```
.
├── src/
│   └── comet_sdkp/
│       ├── CDP4Adaptor.py
│       ├── __init__.py
│       ├── py.typed
│       └── libs/
│           └── (native libraries)
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   └── test_CDP4Adaptor.py
│   ├── smoke/
│   │   ├── __init__.py
│   │   └── test_imports.py
│   └── integration/
│       └── test_CDP4Adaptor_integration.py
├── docs/
│   ├── conf.py
│   ├── index.md
│   ├── contributing.md
│   ├── api/
│   │   ├── index.md
│   │   └── comet_sdkp.md
│   ├── guides/
│   │   ├── faq.md
│   │   ├── installation.md
│   │   ├── getting_started.md
│   │   ├── examples.md
│   │   └── troubleshooting.md
│   ├── _build/
│   ├── make.bat
│   └── Makefile
├── examples/
│   └── script.py
├── .gitignore
├── LICENSE
├── README.md
└── pyproject.toml
```

---

## 💡 Basic Usage Examples

### Example 1: List All Models

```python
from comet_sdkp.CDP4Adaptor import Cdp4SessionService

service = Cdp4SessionService()

# open() returns None on success, error string on failure
result = service.open("http://localhost:5000", "admin", "password")

if result is None:
    print("✓ Connected successfully")
    
    models = service.getParticipantModels()
    print(f"Found {len(models)} models:")
    for model in models:
        print(f"  - {model.Name}")
    
    service.close()
else:
    print(f"✗ Failed to connect: {result}")
```

### Example 2: Navigate Model Hierarchy

```python
from comet_sdkp.CDP4Adaptor import (
    Cdp4SessionService,
    computeProductTree,
    InvalidParametersException,
)

service = Cdp4SessionService()
result = service.open("http://localhost:5000", "admin", "password")

if result is None:
    try:
        models = service.getParticipantModels()
        if models:
            model = models[0]
            domains = service.getAvailableDomains(model)
            
            if domains:
                iteration = service.openActiveIteration(model, domains[0])
                
                if iteration and hasattr(iteration, 'Option') and iteration.Option:
                    tree = computeProductTree(iteration, iteration.Option[0])
                    print(f"✓ Product tree has {len(tree)} root elements")
    except InvalidParametersException as e:
        print(f"✗ Error: {e}")
    finally:
        service.close()
else:
    print(f"✗ Failed to connect: {result}")
```

### Example 3: Filter and Modify Parameters

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
        # ... (open iteration) ...
        models = service.getParticipantModels()
        model = models[0]
        domains = service.getAvailableDomains(model)
        iteration = service.openActiveIteration(model, domains[0])
        
        if iteration and iteration.Option:
            tree = computeProductTree(iteration, iteration.Option[0])
            
            # Find elements with Mass parameter
            mass_elements = getElementByParameterTypeWhereAllValuesAreSet(tree, "Mass")
            print(f"Found {len(mass_elements)} elements with Mass")
            
            # Prepare for modifications
            cloned_iteration, transaction = prepareTransaction(iteration)
            
            # Modify values
            for element in mass_elements:
                if hasattr(element, 'NestedParameter') and element.NestedParameter:
                    for param in element.NestedParameter:
                        if hasattr(param, 'ValueSet'):
                            for value_set in param.ValueSet:
                                setValue(value_set, ParameterSwitchKind.MANUAL, ["100.0"])
            
            # Write changes back to service
            write_result = service.write(transaction)
            if write_result is None:
                print("✓ Changes written successfully")
            else:
                print(f"✗ Write failed: {write_result}")
                
    except InvalidParametersException as e:
        print(f"✗ Error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    finally:
        service.close()
else:
    print(f"✗ Failed to connect: {result}")
```

For more examples, see [examples/script.py](examples/script.py) or [Examples Guide](docs/guides/examples.md).

---

## 🧪 Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition.git
cd COMET-SDKP-Community-Edition

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e ".[dev]"
```

### Running Code Quality Checks

Before submitting code, run the quality checks:

```bash
# Type checking
mypy src/comet_sdkp/ --show-error-codes --pretty

# Code formatting check
black src/ tests/ examples/ --check

# Import sorting check
isort src/ tests/ examples/ --check-only

# Linting
pylint src/comet_sdkp/ --rcfile=pyproject.toml

# Run all tests with coverage
pytest tests/ -v --cov=comet_sdkp --cov-report=term-missing
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run only unit tests (fastest)
pytest tests/unit/ -v

# Run unit + smoke tests (no external dependencies)
pytest tests/ -m "not integration" -v

# Run integration tests (requires CDP4 server at localhost:5000)
pytest tests/integration/ -v

# Run with coverage report
pytest tests/ --cov=comet_sdkp --cov-report=html

# Run specific test file
pytest tests/unit/test_CDP4Adaptor.py -v

# Run specific test
pytest tests/unit/test_CDP4Adaptor.py::TestCdp4SessionServiceOpen::test_open_with_valid_parameters -v

# Run with detailed output
pytest tests/ -vv --tb=long
```

### Test Markers

Tests are organized with markers for selective execution:

- `@pytest.mark.unit` - Fast unit tests with no external dependencies
- `@pytest.mark.smoke` - Basic import and startup tests
- `@pytest.mark.integration` - Tests requiring external resources (CDP4 server)
- `@pytest.mark.slow` - Tests that take longer to execute

```bash
# Run all tests except integration
pytest -m "not integration"

# Run only integration tests
pytest -m integration

# Run unit and smoke tests
pytest -m "unit or smoke"

# Run quick tests (exclude slow)
pytest -m "not slow"
```

### Code Quality Tools

The project uses standard Python development tools:

```bash
# Format code to PEP 8 standards
black src/ tests/ examples/

# Automatically sort and group imports
isort src/ tests/ examples/

# Check type hints
mypy src/comet_sdkp/ --show-error-codes --pretty

# Lint code for style issues
pylint src/comet_sdkp/ --rcfile=pyproject.toml

# Check code coverage
pytest tests/ --cov=comet_sdkp --cov-report=html
coverage report  # View report in terminal
```

### Building Documentation

```bash
# Install documentation tools
pip install -e ".[docs]"

# Build HTML
cd docs
make html          # On Linux/macOS
make.bat html      # On Windows

# View the documentation
start _build/html/index.html      # Windows
open _build/html/index.html       # macOS
xdg-open _build/html/index.html   # Linux

# Or serve locally
python -m http.server -d _build/html 8000
# Then visit http://localhost:8000
```

---

## 🆘 Support

### Documentation & Help

- 📖 **Local Documentation**: See `docs/` directory or build locally
- 📚 **Getting Started Guide**: [docs/guides/getting_started.md](docs/guides/getting_started.md)
- 💡 **Examples**: [examples/script.py](examples/script.py) or [docs/guides/examples.md](docs/guides/examples.md)
- ❓ **FAQ**: [docs/guides/faq.md](docs/guides/faq.md)
- 🔧 **Troubleshooting**: [docs/guides/troubleshooting.md](docs/guides/troubleshooting.md)

### CDP4-COMET Resources

- 📖 **[COMET Development Documentation](https://comet-dev-docs.mbsehub.org/)** - Official documentation for CDP4-COMET
- 🔗 **[COMET SDK Wiki](https://github.com/STARIONGROUP/COMET-SDK-Community-Edition/wiki)** - SDK integration guide
- 📚 **[CDP4-COMET Repository](https://github.com/STARIONGROUP/CDP4-COMET)** - Main platform source code

### Report Issues

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition/discussions)
- 📧 **Contact**: Open an issue or discussion on GitHub

---

## 🎯 Project Status

| Aspect | Status |
|--------|--------|
| **Development** | Active |
| **Stability** | Stable (v0.1.0) |
| **API Stability** | Considered stable for documented features |
| **Support** | Community-based |
| **Python Version** | 3.12+ required |
| **Test Coverage** | 85%+ |

---

## 📝 Changelog

### v0.1.0 (Initial Release - January 2026)

**Features:**
- ✨ Initial public release
- 🎯 Core session management (`Cdp4SessionService`)
- 📊 Product tree navigation (`computeProductTree`)
- 🔍 Parameter filtering (`getElementByParameterType`, `getElementByParameterTypeWhereAllValuesAreSet`)
- ✏️ Transaction support (`prepareTransaction`, `setValue`)
- 📚 Complete documentation with examples
- 🧪 Comprehensive test suite (88+ tests, 85%+ coverage)
- 🔒 Full type hints with mypy support
- 🛠️ Development tools (pytest, black, isort, mypy, pylint)

**Bug Fixes:**
- Fixed enum handling in `setValue()` for .NET enums
- Improved error handling in session operations
- Better type conversion for .NET IEnumerable types

**Breaking Changes:**
- None (initial release)

**Known Issues:**
- None reported

For detailed changelog and commits, see [GitHub Releases](https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition/releases).

---

## 👥 Authors

**STARION GROUP**

- 🌐 Website: [stariongroup.eu](https://www.stariongroup.eu)
- 📧 Email: [contact@stariongroup.eu](mailto:contact@stariongroup.eu)
- 🐙 GitHub: [@STARIONGROUP](https://github.com/STARIONGROUP)

---

## 🙏 Acknowledgments

- CDP4 and COMET development team at ESA and collaborators
- pythonnet for .NET/Python integration
- Python community and open source contributors
- All contributors and users for feedback and support

---

**Last Updated**: January 2026  
**Repository**: [COMET-SDKP-Community-Edition](https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition)  
**License**: LGPL-2.1
