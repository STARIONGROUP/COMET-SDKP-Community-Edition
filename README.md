![CDP4-COMET-Logo](https://raw.githubusercontent.com/STARIONGROUP/COMET-WebServices-Community-Edition/master/COMET-Community-Edition.jpg)

# COMET SDKP (Comunity Edition)

Python wrapper for the COMET native SDK, providing a clean, Pythonic interface to interact with 
the COMET runtime.
 
This repository contains the **Community Edition** of the COMET Python SDK, focused on stability,
clarity, and open usage.
 
---
 
## Features
 
- Pythonic API
- Thin wrapper over native COMET libraries
- Bundled native binaries
- Modern packaging (`pyproject.toml`)
- Full documentation with Sphinx + MyST
- Automated testing with pytest
 
---
 
## Project Status
 
**Current status:** Early public release  
**Stability:** API considered stable for documented features  
**Support:** Community-based
 
Enterprise-specific features and support are intentionally excluded.
 
---
 
## Installation

### Creation of wheel file

To create the wheel file execute the following command inside source code directory.

```bash
python -m build
```

This will create the `.whl` and the `tar.gz` file inside `~/dist` directory.
 
### From python wheel
 
```bash
pip install comet_sdkp-0.1.0-py3-none-any.whl
```

### From source

```bash
git clone https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition.git
cd COMET-SDKP-Community-Edition
pip install .
```

For detailed installation instructions, including native dependencies, see: ```docs/installation.md```

---

## Quick Example

Executable usage examples are provided in the examples/ directory.

---

## Documentation
Full documentation is available in the docs/ directory and includes:
* Installation guide
* Quickstart
* Architecture overview
* Configuration reference
* API reference

To build the documentation locally:
```bash
cd docs
make html
```

---

## Project Structure

```css
.
├── src/
│   └── comet_sdk/
│       ├── client/
│       ├── bindings/
│       ├── native/
│       └── exceptions.py├── tests/
│   ├── unit/
│   ├── integration/
│   └── smoke/
├── docs/
├── examples/
├── pyproject.toml├── pytest.ini└── README.md 
```

---

## Development

### Setup development environment

```bash
python -m venv .venvsource .venv/bin/activate
pip install -e .[dev]
```

### Run tests

```bash
pytest
```

Exclude integration tests:

```bash
pytest -m "not integration" 
```

---

## Contributing
Contributions are welcome.

---

## License
This project is licensed under the LGPL-2.1 license.
See the LICENSE file for details.

---

## Disclaimer
This is a community-maintained SDK.

The authors are not responsible for misuse or deployment in production environments
without proper validation.
 