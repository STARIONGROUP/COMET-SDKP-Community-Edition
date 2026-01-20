# COMET SDKP Community Edition

Welcome to the **COMET SDKP Community Edition** documentation!

This is a Python SDK that provides bindings to the CDP4 (COMET Data Exchange Protocol) via the C++ SDK, enabling seamless integration between COMET and other systems.

## 🚀 Quick Start

```python
from comet_sdkp.CDP4Adaptor import Cdp4SessionService

# Initialize service
service = Cdp4SessionService()

# Connect to CDP4 server
service.open("http://localhost:5000", "admin", "password")

# Get available models
models = service.getParticipantModels()
print(f"Found {len(models)} models")
```

## 📚 Documentation

### Getting Started
- [Installation Guide](guides/installation.md) - Install and configure the SDK
- [Getting Started Guide](guides/getting_started.md) - Your first CDP4 project
- [Examples](guides/examples.md) - Practical code examples

### API Reference
- [Cdp4SessionService](api/comet_sdkp.md) - Main service class and utility functions
- [API Index](api/index.md) - Complete API overview

### Additional Resources
- [Architecture](architecture/overview.md) - System design and architecture
- [FAQ](guides/faq.md) - Frequently asked questions
- [Troubleshooting](guides/troubleshooting.md) - Common issues and solutions
- [Contributing Guide](contributing.md) - How to contribute to the project

## ✨ Features

- **Session Management** - Connect to CDP4 servers and manage sessions
- **Product Tree Navigation** - Compute and traverse nested element hierarchies  
- **Parameter Filtering** - Filter elements by parameter types and values
- **Transaction Support** - Prepare and execute transactions for data modifications
- **Domain Support** - Work with multiple domains of expertise
- **Error Handling** - Comprehensive error handling and logging
- **Type Hints** - Full type hint support for IDE autocomplete
- **Complete Tests** - Unit, integration, and smoke tests

## 📦 Requirements

- Python 3.12+
- pythonnet >= 3.0.5 (automatically installed)
- Access to a CDP4 server (for full functionality)

## 🔗 External Resources

### CDP4-COMET Data Model

For information about CDP4-COMET concepts, data model, and types:

- 📖 **[COMET Development Documentation](https://comet-dev-docs.mbsehub.org/)** - Official documentation for CDP4-COMET
- 🔗 **[COMET SDK Wiki](https://github.com/STARIONGROUP/COMET-SDK-Community-Edition/wiki)** - SDK integration guide and examples
- 📚 **[CDP4-COMET Repository](https://github.com/STARIONGROUP/CDP4-COMET)** - Main COMET platform source code

### Get the SDK

- 🐙 **[GitHub Repository](https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition)** - Clone and install from source
- 📦 **[Releases](https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition/releases)** - Pre-built distributions

## 🎯 Quick Links

- [Installation](guides/installation.md) - Get started in 5 minutes
- [Getting Started](guides/getting_started.md) - Comprehensive tutorial
- [Examples](guides/examples.md) - Copy-paste ready code samples
- [API Reference](api/comet_sdkp.md) - Complete API documentation
- [FAQ](guides/faq.md) - Common questions answered

## 📖 Table of Contents

```{toctree}
:maxdepth: 2
:hidden:

guides/installation
guides/getting_started
guides/examples
api/index
guides/faq
guides/troubleshooting
architecture/overview
contributing
```

## Support

- 📧 **Issues**: [GitHub Issues](https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition/discussions)
- 📚 **COMET Docs**: [Official COMET Documentation](https://comet-dev-docs.mbsehub.org/)

---

**SDK Version**: 0.1.0  
**Python Version**: 3.12+  
**Last Updated**: January 2026  
**License**: LGPL-2.1
