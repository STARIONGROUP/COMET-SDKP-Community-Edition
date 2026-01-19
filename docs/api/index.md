# API Reference

Complete API documentation for COMET SDKP.

## Overview

The COMET SDKP API consists of:

- **1 Main Class**: `Cdp4SessionService` - Primary interface for CDP4 interactions
- **5 Utility Functions**: Helper functions for common operations
- **CDP4 Type Objects**: Imported from the CDP4 libraries via pythonnet

```{toctree}
:maxdepth: 3

comet_sdkp
```

## Quick Reference

### Session Management
- `Cdp4SessionService()` - Create a new service instance
- `Cdp4SessionService.open()` - Connect to a CDP4 server
- `Cdp4SessionService.isSessionOpen` - Check connection status

### Model and Domain Operations
- `Cdp4SessionService.getParticipantModels()` - List assigned models
- `Cdp4SessionService.getAvailableDomains()` - List domains for a model
- `Cdp4SessionService.openActiveIteration()` - Open an iteration

### Data Operations
- `computeProductTree()` - Generate element hierarchy
- `getElementByParameterType()` - Filter elements by parameter
- `getElementByParameterTypeWhereAllValuesAreSet()` - Filter with complete data

### Modification Operations
- `prepareTransaction()` - Prepare for data changes
- `setValue()` - Modify parameter values
- `Cdp4SessionService.write()` - Write changes to server

## Module Structure

```
comet_sdkp/
├── __init__.py
├── CDP4Adaptor.py
│   ├── Cdp4SessionService (class)
│   ├── computeProductTree() (function)
│   ├── getElementByParameterType() (function)
│   ├── getElementByParameterTypeWhereAllValuesAreSet() (function)
│   ├── prepareTransaction() (function)
│   └── setValue() (function)
└── ... (internal modules)
```

## Common Patterns

### Connect and Retrieve Data
```python
service = Cdp4SessionService()
service.open("http://localhost:5000", "user", "pass")
models = service.getParticipantModels()
```

### Navigate Hierarchy
```python
domains = service.getAvailableDomains(model)
iteration = service.openActiveIteration(model, domain)
tree = computeProductTree(iteration, option)
```

### Filter and Modify
```python
elements = getElementByParameterType(tree, "Mass")
iteration, transaction = prepareTransaction(iteration)
# ... make changes ...
service.write(transaction)
```

## See Also

- [Getting Started Guide](../guides/getting_started.md)
- [Installation Guide](../guides/installation.md)
- [Examples](../guides/examples.md)
- [FAQ](../guides/faq.md)