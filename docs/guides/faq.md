# Frequently Asked Questions

## General Questions

### What is COMET SDKP?

COMET SDKP (Community Edition) is a Python SDK that provides bindings to the CDP4 (COMET Data Exchange Protocol). It enables Python developers to interact with CDP4 servers programmatically without needing to write C# code.

### What can I do with this SDK?

You can:
- Connect to CDP4 servers
- Retrieve models and iterations
- Navigate product hierarchies
- Filter elements by parameters
- Modify parameter values
- Write changes back to the server

### Is this production-ready?

The SDK is actively maintained and suitable for production use. However, always test thoroughly in your environment before deploying to production.

### Where can I get help?

- **Documentation**: Read this documentation
- **Examples**: Check the [examples](examples.md)
- **GitHub Issues**: [Report bugs](https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition/issues)
- **Discussions**: Join [GitHub Discussions](https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition/discussions)
- **COMET Documentation**: [Official COMET Docs](https://comet-dev-docs.mbsehub.org/)

## Installation Questions

### What is the easiest way to install?

**Wheel file installation** is the easiest method:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install comet_sdkp-0.1.0-py3-none-any.whl
```

See [Installation Guide](installation.md) for detailed instructions.

### Where do I get the wheel file?

The wheel file is available from:
- Your distribution source
- You can build it yourself using `python -m build`

### How do I install from the wheel file?

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# 3. Install the wheel
pip install comet_sdkp-0.1.0-py3-none-any.whl

# 4. Verify
python -c "from comet_sdkp.CDP4Adaptor import Cdp4SessionService; print('✓ Success')"
```

### Can I install without a wheel file?

Yes, you can install from source:

```bash
git clone https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition.git
cd COMET-SDKP-Community-Edition
pip install .
```

### What are the system requirements?

- **Python**: 3.12 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: Minimum 512MB
- **Disk**: Minimum 100MB
- **Network**: Access to a CDP4 server (for runtime)

### Do I need to install CDP4?

No, you just need access to a running CDP4 server. You don't need to install the full CDP4 application locally.

### Can I use this with Python 3.11?

The SDK requires Python 3.12+. Check your version with `python --version`. If you need 3.11 support, please open a GitHub issue.

### What about macOS and Linux?

The SDK works on all major platforms. The installation steps are the same - just use `source venv/bin/activate` instead of `venv\Scripts\activate` on Windows.

### How do I create a virtual environment?

```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Deactivate
deactivate
```

Virtual environments are recommended to avoid conflicts with other Python packages.

## Usage Questions

### How do I connect to a local CDP4 server?

```python
service = Cdp4SessionService()
service.open("http://localhost:5000", "username", "password")
```

### How do I connect to a remote server?

```python
service.open("https://cdp4.company.com", "username", "password")
```

### What if I get a "Session already open" error?

Close the existing session first:

```python
if service.isSessionOpen:
    service.isSessionOpen = False
    service.session = None

service.open(url, username, password)
```

### How do I list all available models?

```python
models = service.getParticipantModels()
for model in models:
    print(model.Name)
```

### How do I open an iteration?

```python
# First get the model and domain
model = models[0]
domains = service.getAvailableDomains(model)

# Then open the iteration
iteration = service.openActiveIteration(model, domains[0])
```

### How do I modify a parameter value?

```python
from comet_sdkp.CDP4Adaptor import prepareTransaction, setValue
from CDP4Common.EngineeringModelData import ParameterSwitchKind

# Prepare transaction
iteration, transaction = prepareTransaction(iteration)

# Set new value
setValue(value_set, ParameterSwitchKind.MANUAL, ["100"])

# Write to server
service.write(transaction)
```

## API Questions

### What's the difference between MANUAL, COMPUTED, and REFERENCE?

- **MANUAL** - User-provided values
- **COMPUTED** - Values calculated from a formula
- **REFERENCE** - Reference to another parameter's value

### What does getParticipantModels() return?

Returns a list of engineering models assigned to the current user account.

### What does getAvailableDomains() return?

Returns a list of domains of expertise that the user can work with in the selected model.

### What is a NestedElement?

A NestedElement is a hierarchical representation of elements within an iteration. It represents the product tree structure.

### What is a Transaction?

A transaction groups multiple changes together. It allows atomic writes to the server - either all changes succeed or all fail.

## Data Questions

### What's the difference between Iteration and Option?

- **Iteration** - A version of an engineering model (like a checkpoint)
- **Option** - A variation within an iteration (alternative designs or configurations)

### What is ParameterType?

A ParameterType defines the characteristics of a parameter (name, unit, data type, etc.). Parameters are instances of ParameterTypes assigned to elements.

### What is an ActualValue?

ActualValue is the current value of a parameter. It can be:
- A number (e.g., "100")
- A string (e.g., "Component A")
- Unset (represented as "-")

## CDP4-COMET Questions

### Where can I learn about the CDP4-COMET data model?

See the official resources:
- 📖 **[COMET Development Documentation](https://comet-dev-docs.mbsehub.org/)** - Comprehensive COMET documentation
- 🔗 **[COMET SDK Wiki](https://github.com/STARIONGROUP/COMET-SDK-Community-Edition/wiki)** - SDK integration guide
- 📚 **[CDP4-COMET Repository](https://github.com/STARIONGROUP/CDP4-COMET)** - Source code and examples

### What is CDP4?

CDP4 (COMET Data Exchange Protocol) is a protocol for exchanging engineering data. COMET is the platform that implements it.

### How do I find out about CDP4 types and classes?

See [COMET Development Documentation](https://comet-dev-docs.mbsehub.org/) for detailed information about all CDP4 types, enums, and classes.

## Testing Questions

### How do I write unit tests?

Use mocks for CDP4 objects:

```python
from unittest.mock import MagicMock, patch

def test_get_models():
    service = Cdp4SessionService()
    service.isSessionOpen = True
    service.session = MagicMock()
    
    mock_model = MagicMock()
    mock_model.Name = "Test Model"
    
    service.session.RetrieveSiteDirectory.return_value.Model = [mock_model]
    
    models = service.getParticipantModels()
    assert len(models) == 1
```

### How do I test with a real server?

Mark tests with `@pytest.mark.integration`:

```python
@pytest.mark.integration
def test_real_connection():
    service = Cdp4SessionService()
    service.open("http://localhost:5000", "admin", "password")
    assert service.isSessionOpen
```

Run with: `pytest tests/ -m integration`

### What are the test markers?

- `@pytest.mark.unit` - Fast unit tests with no external dependencies
- `@pytest.mark.smoke` - Basic import and startup tests
- `@pytest.mark.integration` - Tests requiring external resources

## Performance Questions

### How do I improve performance with large datasets?

1. **Filter early**: Filter elements before processing
2. **Cache results**: Reuse computed trees
3. **Batch operations**: Group modifications in transactions
4. **Limit scope**: Work with specific options/iterations

### How much data can I handle?

This depends on:
- Available memory (RAM)
- Network bandwidth
- Server performance
- Size of the model

For models with thousands of elements, filtering and batching are essential.

## Advanced Questions

### Can I use this with async/await?

Currently, the SDK uses synchronous APIs. Async support is planned for future releases. For now, use threading if you need async behavior.

### Can I extend the SDK?

Yes! The SDK is open source. You can:
- Subclass `Cdp4SessionService`
- Create wrapper functions
- Contribute improvements to the project

### How do I contribute?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

See [Contributing Guide](../contributing.md) for details.

## More Help

- 📖 [Getting Started](getting_started.md)
- 💡 [Examples](examples.md)
- 🔧 [Troubleshooting](troubleshooting.md)
- 📚 [API Reference](../api/comet_sdkp.md)
- 🌐 [COMET Documentation](https://comet-dev-docs.mbsehub.org/)