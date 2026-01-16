 
# Installation

This document describes how to install the **COMET SDKP – Community Edition** Python SDK,
including system requirements, supported platforms, and common installation issues.
The SDK is designed to be **self-contained**: all required native libraries are bundled
with the Python package and loaded automatically at runtime.

---

## Supported Platforms

The SDK currently supports the following environments:
| Platform | Architecture | Status |
|--------|--------------|--------|
| Windows | x86_64       | Supported |
| Linux  | x86_64       | Not yet Supported |
| macOS  | x86_64 / arm64 | Not yet Supported |
> Other platforms or architectures may work but are not officially supported.

---

## Python Requirements

- Python **3.12 or newer**
- `pip` 25.0 or newer (recommended)

You can verify your Python version with:

```bash
python --version
```
## Installation from wheel

The recommended way to install the SDK is via wheel using pip:

```bash
pip install comet_sdkp-0.1.0-py3-none-any.whl
```

This will:
* Install the Python package
* Install all required runtime dependencies
* Deploy the appropriate native libraries for your platform

No additional system configuration is required.

---

## Verifying the Installation

After installation, you can verify that the SDK is available:

```bash
python -c "import comet_sdkp; print(comet_sdkp.__version__)"
```

If no error is raised, the installation was successful.

---

## Native Libraries

COMET SDKP relies on platform-specific native libraries to provide low-level functionality.

### How native libraries are handled

* Native binaries (.dll) are bundled inside the Python package.
* The correct binary is selected automatically based on the operating system.
* Libraries are loaded lazily (only when required).
* Users do not need to install system-wide dependencies.

### Binary formats by platform

| Operating System | Binary Format |
|------------------|---------------|
| Windows | .dll |
| Linux	| .so |
| macOS	| .dylib |

---

## Virtual Environments (Recommended)

Although not strictly required, using a virtual environment is strongly recommended.

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate it

#### Linux / macOS

```bash
source .venv/bin/activate
```

#### Windows (PowerShell)

```bash
.venv\Scripts\Activate.ps1
```

Then install the SDK:

```bash
pip install comet-sdkp
```

---

## Installation for Development

If you are contributing to the SDK or working from source, install it in editable mode.

### Clone the repository

```bash
git clone https://github.com/<org>/COMET-SDKP-Community-Edition.git
cd COMET-SDKP-Community-Edition
```

Install with development dependencies

```bash
pip install -e .[dev,docs]
```

This installs:
* The SDK in editable mode.
* Test dependencies.
* Documentation tooling (Sphinx, MyST, theme).

---

## Building the Documentation Locally

To build the documentation locally:

```bash
sphinx-build -b html docs docs/_build/html
```

Open the generated documentation:

```text
docs/_build/html/index.html
```

---

## Common Installation Issues

```ImportError: cannot load native library```

Possible causes:
* Unsupported platform or architecture.
* Corrupted installation.
* Incomplete wheel download.

Recommended actions:
1. Ensure your platform is officially supported.
2. Reinstall the package:
    ```bash
    pip install --force-reinstall comet-sdkp
    ```
3. Verify that the comet_sdkp/libs/ directory exists inside site-packages.

---

## Antivirus or Endpoint Protection Software (Windows)

Some antivirus or endpoint protection tools may block the loading of native libraries.

If you encounter unexpected load failures:
* Add the Python virtual environment to the allowlist.
* Ensure the installation directory is not quarantined.

---

## pip or SSL Errors

Ensure your pip installation is up to date:

```bash
python -m pip install --upgrade pip
```

---

## Uninstallation

To remove the SDK:

```bash
pip uninstall comet-sdkp
```

This will remove both the Python package and the bundled native libraries.

---

## Next Steps

* Continue with the Quickstart Guide.
* Review the API Reference.
* Learn about the internal architecture in Native Libraries.

---

## Support

For bugs, feature requests, or questions:
* Open an issue on GitHub.
* Provide your OS, Python version, and error message.
* Clear reproduction steps help us help you faster.
 