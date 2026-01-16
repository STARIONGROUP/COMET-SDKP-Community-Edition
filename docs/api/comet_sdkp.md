# COMET SDKP API Reference
 
This document provides the API reference for the **COMET SDK Python Community Edition**.
 
The library is implemented in `src/comet_sdkp/CDP4Adaptor.py` and exposes:
 
- One main class: `Cdp4SessionService`
- Several standalone functions
 
All other modules are internal and not part of the public API.
 
---
 
## Importing the SDK
 
```python
from comet_sdkp.CDP4Adaptor import Cdp4SessionService, <function1>, <function2>
```

Replace `<function1>` and `<function2>` with the actual function names exported by the module.

---

## Class Reference
 
### `Cdp4SessionService`
 
```{autoclass} comet_sdkp.CDP4Adaptor.Cdp4SessionService
:members:
:undoc-members:
:show-inheritance:
```
 
### Description:
 
Cdp4SessionService provides a high-level interface to the COMET backend through a session manager.
It wraps lower-level functions and handles connection, reading, and writing of data in a Pythonic way.

## Function Reference

```{automodule} comet_sdkp.CDP4Adaptor
:members:
:undoc-members:
:show-inheritance:
:exclude-members: Cdp4SessionService
```
 
## Next Steps
 
For detailed guides on usage, see:
 
- [Installation](../guides/installation.md)