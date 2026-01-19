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
service.open("http://localhost:5000", "admin", "password")

if service.isSessionOpen:
    # Get available models
    models = service.getParticipantModels()
    print(f"✓ Found {len(models)} models")
    
    # List them
    for model in models:
        print(f"  - {model.Name}")
else:
    print("✗ Failed to connect")
```

### 3. Run Your Script

```bash
python script.py
```

Expected output:
```
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

### Method 3: Development Installation

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
- Access to testing tools
- Can build documentation locally
- Can contribute to the project

### Method 4: Build Wheel File Locally

If you want to build a wheel file from source:

```bash
# Clone the repository
git clone https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition.git
cd COMET-SDKP-Community-Edition

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
# Documentation tools (to build docs locally)
pip install sphinx myst-parser

# Development tools (testing, linting)
pip install pytest pytest-cov flake8 black

# Both (from source installation)
pip install -e ".[dev,docs]"
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
pip install sphinx myst-parser

# Build HTML documentation
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
COMET-SDKP-Community-Edition/
├── comet_sdkp/                          # Main package
│   ├── __init__.py
│   └── CDP4Adaptor.py                   # Core module with all public APIs
│
├── tests/                               # Test suite
│   ├── unit/                            # Unit tests (no external dependencies)
│   │   └── test_CDP4Adaptor.py
│   ├── integration/                     # Integration tests (require CDP4 server)
│   │   └── test_CDP4Adaptor_integration.py
│   └── smoke/                           # Basic smoke tests
│       └── test_smoke.py
│
├── docs/                                # Documentation
│   ├── guides/                          # User guides
│   │   ├── installation.md
│   │   ├── getting_started.md
│   │   ├── examples.md
│   │   ├── faq.md
│   │   └── troubleshooting.md
│   ├── api/                             # API reference
│   │   ├── index.md
│   │   └── comet_sdkp.md
│   ├── architecture/                    # Architecture documentation
│   │   └── overview.md
│   ├── conf.py                          # Sphinx configuration
│   ├── index.md                         # Documentation homepage
│   └── Makefile / make.bat              # Build scripts
│
├── examples/                            # Example scripts
│   ├── basic_connection.py
│   ├── list_models.py
│   └── compute_product_tree.py
│
├── .github/                             # GitHub configuration
│   └── workflows/                       # CI/CD workflows
│
├── pyproject.toml                       # Project configuration and dependencies
├── setup.py                             # Setup script (auto-generated)
├── pytest.ini                           # pytest configuration
├── README.md                            # This file
├── LICENSE                              # LGPL-2.1 License
└── .gitignore                           # Git ignore rules
```

---

## 💡 Basic Usage Examples

### Example 1: List All Models

```python
from comet_sdkp.CDP4Adaptor import Cdp4SessionService

service = Cdp4SessionService()

if service.open("http://localhost:5000", "admin", "password"):
    models = service.getParticipantModels()
    
    print(f"Found {len(models)} models:")
    for model in models:
        print(f"  - {model.Name}")
else:
    print("Failed to connect")
```

### Example 2: Navigate Model Hierarchy

```python
from comet_sdkp.CDP4Adaptor import Cdp4SessionService, computeProductTree

service = Cdp4SessionService()
service.open("http://localhost:5000", "admin", "password")

models = service.getParticipantModels()
if models:
    model = models[0]
    domains = service.getAvailableDomains(model)
    
    if domains:
        iteration = service.openActiveIteration(model, domains[0])
        
        if iteration and iteration.Option:
            tree = computeProductTree(iteration, iteration.Option[0])
            print(f"Product tree has {len(tree)} elements")
```

### Example 3: Filter and Modify Parameters

```python
from comet_sdkp.CDP4Adaptor import (
    Cdp4SessionService,
    computeProductTree,
    getElementByParameterType,
    prepareTransaction,
    setValue,
)
from CDP4Common.EngineeringModelData import ParameterSwitchKind

service = Cdp4SessionService()
service.open("http://localhost:5000", "admin", "password")

# ... (open iteration) ...

tree = computeProductTree(iteration, option)

# Find elements with Mass parameter
mass_elements = getElementByParameterType(tree, "Mass")
print(f"Found {len(mass_elements)} elements with Mass")

# Prepare for modifications
iteration, transaction = prepareTransaction(iteration)

# Modify values
for element in mass_elements:
    for param in element.NestedParameter:
        setValue(param, ParameterSwitchKind.MANUAL, ["100.0"])

# Write changes
result = service.write(transaction)
if result is None:
    print("✓ Changes written successfully")
else:
    print(f"✗ Write failed: {result}")
```

For more examples, see the [Examples Guide](docs/guides/examples.md).

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
```

### Test Markers

Tests are organized with markers for selective execution:

- `@pytest.mark.unit` - Fast unit tests with no external dependencies
- `@pytest.mark.smoke` - Basic import and startup tests
- `@pytest.mark.integration` - Tests requiring external resources (CDP4 server)

```bash
# Run all tests except integration
pytest -m "not integration"

# Run only integration tests
pytest -m integration

# Run unit and smoke tests
pytest -m "unit or smoke"
```

### Code Style

The project follows PEP 8 conventions:

```bash
# Check code style
flake8 comet_sdkp tests

# Format code
black comet_sdkp tests

# Check type hints
mypy comet_sdkp
```

### Building Documentation

```bash
# Install documentation tools
pip install -e ".[docs]"

# Build HTML
cd docs
make html

# View
start _build/html/index.html  # Windows
open _build/html/index.html   # macOS
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/contributing.md) for details on:

- How to report bugs
- How to suggest features
- How to submit code changes
- Development workflow
- Code standards

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Write tests for new functionality
5. Run tests: `pytest`
6. Update documentation
7. Commit with clear message: `git commit -m "Add: clear description"`
8. Push to your fork: `git push origin feature/your-feature-name`
9. Open a Pull Request

---

## 📄 License

This project is licensed under the **LGPL-2.1 License**.

See the [LICENSE](LICENSE) file for full details.

**Summary:**
- ✓ Free to use and modify
- ✓ Can use in proprietary software
- ✓ Must include license notice
- ✓ Changes must be documented
- ✓ Must provide source code access

---

## ⚠️ Disclaimer

This is a **community-maintained SDK** for the COMET platform.

**Important Notes:**

- The authors are not responsible for misuse or deployment in production environments without proper validation and testing
- Always test thoroughly in your environment before using in production
- The SDK is provided "as-is" without any warranties
- Security vulnerabilities should be reported responsibly to the maintainers
- For enterprise support, please contact STARION GROUP

---

## 🆘 Support

### Documentation & Help

- 📖 **Local Documentation**: See `docs/` directory or build locally
- 📚 **Getting Started Guide**: [docs/guides/getting_started.md](docs/guides/getting_started.md)
- 💡 **Examples**: [docs/guides/examples.md](docs/guides/examples.md)
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

### Related Projects

- 🔗 [CDP4-COMET](https://github.com/STARIONGROUP/CDP4-COMET) - Main COMET platform
- 🔗 [COMET SDK Community Edition](https://github.com/STARIONGROUP/COMET-SDK-Community-Edition) - C# SDK
- 🔗 [STARION GROUP](https://github.com/STARIONGROUP) - Organization GitHub

---

## 🎯 Project Status

| Aspect | Status |
|--------|--------|
| **Development** | Active |
| **Stability** | Stable (v0.1.0) |
| **API Stability** | Considered stable for documented features |
| **Support** | Community-based |
| **Python Version** | 3.12+ required |

---

## 📝 Changelog

### v0.1.0 (Initial Release)

- ✨ Initial public release
- 🎯 Core session management
- 📊 Product tree navigation
- 🔍 Parameter filtering
- ✏️ Transaction support
- 📚 Complete documentation
- 🧪 Comprehensive test suite

For detailed changelog, see [GitHub Releases](https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition/releases).

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
- Community contributors and users

---

**Last Updated**: January 2026  
**Repository**: [COMET-SDKP-Community-Edition](https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition)
