# Installation Guide

This guide will help you install the COMET SDKP Community Edition.

## System Requirements

### Python Version
- **Python 3.12 or higher** (required)
- Check your version with: `python --version`

### Operating System
- Windows (tested on Windows 11)
- macOS (10.14+)
- Linux (Ubuntu 20.04+, etc.)

### Other Requirements
- **pythonnet** >= 3.0.5 (automatically installed)
- **.NET runtime** (for pythonnet integration).  
  - On Windows ensure either .NET Framework (4.7.2+) or .NET 6+ runtime is installed.
  - On macOS/Linux install the appropriate .NET runtime for pythonnet usage.
- Minimum 512MB RAM
- 100MB disk space
- Git (only needed for source installation)

## Installation Methods

### Method 1: Install from Wheel File ⭐ (Recommended)

This is the **preferred and easiest installation method**. Use this if you have the `.whl` file.

**Get the Wheel File:**
- Download `comet_sdkp-0.1.0-py3-none-any.whl` from your distribution source

**Installation Steps:**

```bash
# Step 1: Create virtual environment
python -m venv venv

# Step 2: Activate virtual environment
# On Windows (cmd.exe)
venv\Scripts\activate

# On Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# On POSIX shells (macOS / Linux)
source venv/bin/activate

# Step 3: Install from wheel file
pip install comet_sdkp-0.1.0-py3-none-any.whl

# Step 4: Verify installation
python -c "from comet_sdkp.CDP4Adaptor import Cdp4SessionService; print('✓ SDK installed successfully')"
```

**Why Use Wheel Files?**
- ✅ Fastest installation (no compilation needed)
- ✅ No need to clone the repository
- ✅ Easy to share and distribute
- ✅ Works on any system with Python 3.12+

### Method 2: Install from Source

Use this method if you don't have the wheel file or want the latest development version.

**Installation Steps:**

```bash
# Step 1: Clone the repository
git clone https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition.git
cd COMET-SDKP-Community-Edition

# Step 2: Create virtual environment
python -m venv venv

# Step 3: Activate virtual environment
# On Windows (cmd.exe)
venv\Scripts\activate

# On Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# On POSIX shells (macOS / Linux)
source venv/bin/activate

# Step 4: Install the SDK
pip install .

# Step 5: Verify installation
python -c "from comet_sdkp.CDP4Adaptor import Cdp4SessionService; print('✓ SDK installed successfully')"
```

### Method 3: Development Installation

Use this method if you want to contribute or modify the code.

**Installation Steps:**

```bash
# Step 1: Clone the repository
git clone https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition.git
cd COMET-SDKP-Community-Edition

# Step 2: Create virtual environment
python -m venv venv

# Step 3: Activate virtual environment
# On Windows (cmd.exe)
venv\Scripts\activate

# On Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# On POSIX shells (macOS / Linux)
source venv/bin/activate

# Step 4: Install in development mode with all tools
pip install -e ".[dev]"
```

**Benefits of Development Mode:**
- Code changes take effect immediately
- Access to testing tools (pytest)
- Can build documentation locally
- Can run the full test suite
- Can contribute to the project

### Method 4: Build Wheel File from Source

Use this if you want to create a wheel file locally for distribution.

**Steps:**

```bash
# Step 1: Clone the repository
git clone https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition.git
cd COMET-SDKP-Community-Edition

# Step 2: Install build tools
pip install build

# Step 3: Build the distribution
python -m build

# Step 4: Install from the generated wheel
pip install dist/comet_sdkp-0.1.0-py3-none-any.whl
```

The wheel file will be available in the `dist/` directory for sharing.

## Installation Comparison

| Method | Speed | Requirements | Use Case |
|--------|-------|--------------|----------|
| **Wheel File** | ⚡ Fastest | Python 3.12+ | Production, Easy installation |
| **From Source** | 🐢 Slower | Python 3.12+, Git | Quick setup, No wheel available |
| **Development** | 🐢 Slower | Python 3.12+, Git | Contributing, Extending |
| **Build Wheel** | 🐢 Slower | Python 3.12+, Git | Creating distributions |

## Optional Features

If you need additional functionality beyond the base SDK installation:

```bash
# Documentation tools (to build docs locally)
# Only needed if installing from source
pip install sphinx myst-parser

# Testing tools
# Only needed if installing from source
pip install pytest pytest-cov

# All development tools (from source installation)
pip install -e ".[dev]"

# All documentation tools (from source installation)
pip install -e ".[docs]"
```

## Verify Installation

Test that the SDK is properly installed:

```bash
# Quick test
python -c "from comet_sdkp.CDP4Adaptor import Cdp4SessionService; print('✓ SDK installed successfully')"

# More detailed test
python << EOF
from comet_sdkp.CDP4Adaptor import (
    Cdp4SessionService,
    computeProductTree,
    getElementByParameterType,
    prepareTransaction,
    setValue,
)

print("✓ All main modules imported successfully")
print("✓ Installation verified!")
EOF
```

You should see:
```
✓ SDK installed successfully
```

## Virtual Environments

It's recommended to use a virtual environment to avoid conflicts with other Python packages:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows (cmd.exe):
venv\Scripts\activate

# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# macOS/Linux:
source venv/bin/activate

# You should see (venv) in your prompt
# Install the SDK
pip install comet_sdkp-0.1.0-py3-none-any.whl

# Deactivate when done
deactivate
```

## Troubleshooting

### Error: "No module named 'clr'"

This means pythonnet is not properly installed or the .NET runtime is missing.

**Solution:**
```bash
# Make sure you're in the virtual environment
# Then reinstall pythonnet
pip install --force-reinstall pythonnet>=3.0.5

# On Windows ensure a compatible .NET runtime is installed:
# - .NET Framework 4.7.2+ or .NET 6+ runtime
```

### Error: "No module named 'comet_sdkp'"

The SDK is not installed in your Python environment.

**Solution:**
```bash
# Verify you're in the virtual environment (should see (venv) in prompt)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Then install again
pip install comet_sdkp-0.1.0-py3-none-any.whl
```

### Error: "Python version not supported"

You're using Python 3.11 or older.

**Solution:**
```bash
# Check your Python version
python --version

# Install Python 3.12 or higher from https://www.python.org/downloads/
# Then create a new virtual environment with the new Python version
```

### Error: ".whl file not found"

The wheel file is not in the current directory.

**Solution:**
```bash
# Make sure the wheel file is in your current directory
# Or provide the full path
pip install /path/to/comet_sdkp-0.1.0-py3-none-any.whl

# Check the file exists
ls comet_sdkp-0.1.0-py3-none-any.whl  # macOS/Linux
dir comet_sdkp-0.1.0-py3-none-any.whl # Windows
```

### Error: "Permission denied"

You don't have permission to install packages.

**Solution:**
```bash
# Use a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install comet_sdkp-0.1.0-py3-none-any.whl

# Or use --user flag (not recommended)
pip install --user comet_sdkp-0.1.0-py3-none-any.whl
```

## Next Steps

After successful installation:

1. **Run a quick test**: Use the verification command above
2. **Read the Getting Started guide**: [Getting Started Guide](getting_started.md)
3. **Check the examples**: [Examples](examples.md)
4. **Browse the API Reference**: [API Reference](../api/comet_sdkp.md)

## Getting Help

If you encounter issues:

1. Check [Troubleshooting Guide](troubleshooting.md)
2. Review [FAQ](faq.md)
3. Open a [GitHub Issue](https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition/issues)

## Related Documentation

For information about CDP4-COMET data model and concepts:

- 📖 **[COMET Development Documentation](https://comet-dev-docs.mbsehub.org/)** - Official COMET docs
- 🔗 **[COMET SDK Wiki](https://github.com/STARIONGROUP/COMET-SDK-Community-Edition/wiki)** - SDK guide
- 📚 **[CDP4-COMET Repository](https://github.com/STARIONGROUP/CDP4-COMET)** - Source code
