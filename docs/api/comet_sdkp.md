# COMET SDKP API Reference

Complete API reference for the **COMET SDKP Community Edition**.

## Overview

The COMET SDKP library is implemented in `comet_sdkp/CDP4Adaptor.py` and exposes:

- **1 Main Class**: `Cdp4SessionService` - Session management and data operations
- **5 Utility Functions**: Product tree computation, element filtering, and transactions
- All other modules are internal implementation details

## Importing the SDK

```python
from comet_sdkp.CDP4Adaptor import (
    Cdp4SessionService,
    computeProductTree,
    getElementByParameterType,
    getElementByParameterTypeWhereAllValuesAreSet,
    prepareTransaction,
    setValue,
)
```

## Main Class

### Cdp4SessionService

The primary class for interacting with CDP4 servers.

**Location**: `comet_sdkp.CDP4Adaptor.Cdp4SessionService`

**Purpose**: Manages CDP4 server connections, model retrieval, and data operations.

#### Constructor

```python
service = Cdp4SessionService()
```

Creates a new session service instance. Initializes internal components:
- `session` - CDP4 session object
- `messageBus` - Message communication bus
- `dal` - Data access layer
- `isSessionOpen` - Connection status flag

#### Key Methods

##### `open(uri: str, username: str, password: str) -> str | None`

Connect to a CDP4 server.

**Parameters:**
- `uri` (str) - Server URL (e.g., `"http://localhost:5000"`)
- `username` (str) - User account name
- `password` (str) - User password

**Returns:**
- `None` if successful
- Error message string if failed

**Raises:**
- Network errors if server is unreachable
- Authentication errors if credentials are invalid

**Example:**
```python
service = Cdp4SessionService()
result = service.open("http://localhost:5000", "admin", "password")

if result is None:
    print("Connected successfully")
else:
    print(f"Connection failed: {result}")
```

##### `getParticipantModels() -> list`

Retrieve all models assigned to the current user.

**Returns:**
- List of engineering model objects

**Requires:**
- Session must be open (`isSessionOpen == True`)

**Example:**
```python
if service.isSessionOpen:
    models = service.getParticipantModels()
    for model in models:
        print(f"Model: {model.Name} (ID: {model.Iid})")
```

##### `getAvailableDomains(setup: EngineeringModelSetup) -> list`

Get domains of expertise available for a model.

**Parameters:**
- `setup` (EngineeringModelSetup) - The model setup object

**Returns:**
- List of domain objects

**Raises:**
- `ValueError` if setup parameter is missing

**Example:**
```python
model = models[0]
domains = service.getAvailableDomains(model)

for domain in domains:
    print(f"Domain: {domain.Name}")
```

##### `openActiveIteration(setup: EngineeringModelSetup, domain: DomainOfExpertise) -> Iteration | str`

Open the active iteration for a model and domain.

**Parameters:**
- `setup` (EngineeringModelSetup) - The model setup
- `domain` (DomainOfExpertise) - The domain of expertise

**Returns:**
- Iteration object if successful
- Error message string if failed

**Raises:**
- `ValueError` if setup or domain not provided

**Example:**
```python
iteration = service.openActiveIteration(model, domains[0])

if isinstance(iteration, str):
    print(f"Failed to open iteration: {iteration}")
else:
    print(f"Opened iteration: {iteration.Iid}")
```

##### `write(transaction: ThingTransaction) -> None | str`

Write transaction changes to the server.

**Parameters:**
- `transaction` (ThingTransaction) - The transaction containing changes

**Returns:**
- `None` if successful
- Error message string if failed

**Requires:**
- Session must be open

**Example:**
```python
result = service.write(transaction)

if result is None:
    print("Changes written successfully")
else:
    print(f"Write failed: {result}")
```

#### Properties

##### `isSessionOpen: bool`

Current session connection status.

```python
if service.isSessionOpen:
    # Safe to use service methods
    models = service.getParticipantModels()
```

##### `session`

The underlying CDP4 session object. Provides access to low-level CDP4 functionality.

## Utility Functions

### computeProductTree()

Generate a nested element tree from an iteration.

**Signature:**
```python
def computeProductTree(iteration: Iteration, option: Option) -> list[NestedElement]
```

**Parameters:**
- `iteration` (Iteration) - The iteration containing elements
- `option` (Option) - The option for which to compute the tree

**Returns:**
- List of NestedElement objects representing the product hierarchy

**Raises:**
- `ValueError` if iteration or option not provided

**Example:**
```python
from comet_sdkp.CDP4Adaptor import computeProductTree

tree = computeProductTree(iteration, option)
print(f"Product tree contains {len(tree)} elements")

for element in tree:
    print(f"  - {element.Name}")
```

### getElementByParameterType()

Filter elements that have a specific parameter type.

**Signature:**
```python
def getElementByParameterType(elements: list, parameterTypeName: str) -> list
```

**Parameters:**
- `elements` (list) - List of NestedElement objects to filter
- `parameterTypeName` (str) - Name of the parameter type to match

**Returns:**
- List of elements containing the specified parameter type

**Raises:**
- `ValueError` if elements or parameter type name not provided

**Example:**
```python
from comet_sdkp.CDP4Adaptor import getElementByParameterType

# Find all elements with "Mass" parameter
mass_elements = getElementByParameterType(tree, "Mass")
print(f"Found {len(mass_elements)} elements with Mass parameter")
```

### getElementByParameterTypeWhereAllValuesAreSet()

Filter elements where all values for a parameter type are set.

**Signature:**
```python
def getElementByParameterTypeWhereAllValuesAreSet(
    elements: list,
    parameterTypeName: str
) -> list
```

**Parameters:**
- `elements` (list) - List of elements to filter
- `parameterTypeName` (str) - Parameter type name

**Returns:**
- List of elements with all values set for the parameter

**Note:**
Elements are excluded if any parameter value is "-" (unset).

**Example:**
```python
from comet_sdkp.CDP4Adaptor import getElementByParameterTypeWhereAllValuesAreSet

# Get elements where ALL Mass values are provided
complete = getElementByParameterTypeWhereAllValuesAreSet(mass_elements, "Mass")
print(f"Elements with complete Mass data: {len(complete)}")
```

### prepareTransaction()

Prepare an iteration for modification via a transaction.

**Signature:**
```python
def prepareTransaction(iteration: Iteration) -> tuple[Iteration, ThingTransaction]
```

**Parameters:**
- `iteration` (Iteration) - The iteration to prepare

**Returns:**
- Tuple of (cloned iteration, ThingTransaction)

**Raises:**
- `ValueError` if iteration not provided

**Example:**
```python
from comet_sdkp.CDP4Adaptor import prepareTransaction

iteration, transaction = prepareTransaction(iteration)

# Make modifications...
# Then write changes
service.write(transaction)
```

### setValue()

Set values for a parameter value set.

**Signature:**
```python
def setValue(
    valueSet: ParameterValueSetBase,
    switchKind: ParameterSwitchKind,
    values: list[str]
) -> ParameterValueSetBase
```

**Parameters:**
- `valueSet` (ParameterValueSetBase) - The value set to modify
- `switchKind` (ParameterSwitchKind) - The switch kind controlling how values are used:
  - `MANUAL` - User-provided values
  - `COMPUTED` - Values computed from a formula
  - `REFERENCE` - Reference to another parameter value
- `values` (list[str]) - List of string values to set

**Returns:**
- The modified value set object

**Example:**
```python
from comet_sdkp.CDP4Adaptor import setValue
from CDP4Common.EngineeringModelData import ParameterSwitchKind

# Set manual values
setValue(
    value_set,
    ParameterSwitchKind.MANUAL,
    ["100", "200", "300"]
)

# Or set computed values
setValue(
    value_set,
    ParameterSwitchKind.COMPUTED,
    ["=Mass*Density"]
)
```

## Complete Example

Here's a complete example using the API:

```python
from comet_sdkp.CDP4Adaptor import (
    Cdp4SessionService,
    computeProductTree,
    getElementByParameterType,
    prepareTransaction,
    setValue,
)
from CDP4Common.EngineeringModelData import ParameterSwitchKind

# Initialize service
service = Cdp4SessionService()

# Connect to server
if service.open("http://localhost:5000", "admin", "password"):
    print("✗ Connection failed")
    exit(1)

# Get models
models = service.getParticipantModels()
print(f"✓ Found {len(models)} models")

if not models:
    exit(0)

model = models[0]

# Get domains
domains = service.getAvailableDomains(model)
print(f"✓ Found {len(domains)} domains")

if not domains:
    exit(0)

# Open iteration
iteration = service.openActiveIteration(model, domains[0])
if isinstance(iteration, str):
    print(f"✗ Failed to open iteration: {iteration}")
    exit(1)

print(f"✓ Opened iteration: {iteration.Iid}")

# Compute product tree
if iteration.Option:
    option = iteration.Option[0]
    tree = computeProductTree(iteration, option)
    print(f"✓ Product tree has {len(tree)} elements")
    
    # Filter by parameter
    mass_elements = getElementByParameterType(tree, "Mass")
    print(f"✓ Found {len(mass_elements)} elements with Mass")
    
    # Prepare transaction for modifications
    iteration, transaction = prepareTransaction(iteration)
    
    # Modify values
    for element in mass_elements:
        for param in element.NestedParameter:
            if param.AssociatedParameter.ParameterType.Name == "Mass":
                setValue(param, ParameterSwitchKind.MANUAL, ["50.0"])
    
    # Write changes
    result = service.write(transaction)
    if result is None:
        print(f"✓ Successfully updated {len(mass_elements)} elements")
    else:
        print(f"✗ Write failed: {result}")
```

## Error Handling

All functions may raise exceptions. Always include error handling:

```python
from comet_sdkp.CDP4Adaptor import Cdp4SessionService

service = Cdp4SessionService()

try:
    service.open("http://localhost:5000", "admin", "password")
    
    if not service.isSessionOpen:
        print("Session failed to open")
        exit(1)
    
    models = service.getParticipantModels()
    
except ValueError as e:
    print(f"Parameter error: {e}")
    exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    exit(1)
```

## See Also

- [Installation Guide](../guides/installation.md)
- [Getting Started Guide](../guides/getting_started.md)
- [Examples](../guides/examples.md)
- [Troubleshooting](../guides/troubleshooting.md)