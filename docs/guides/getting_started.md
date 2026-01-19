# Getting Started Guide

This guide will help you get started with the COMET SDKP Community Edition.

## Prerequisites

- Python 3.12 or higher installed
- A CDP4 server instance running and accessible
- Valid CDP4 credentials

## Step-by-Step Tutorial

### Step 1: Create a Python Project

```bash
mkdir my_cdp4_project
cd my_cdp4_project
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install COMET SDKP

```bash
pip install comet-sdkp
```

### Step 3: Write Your First Script

Create a file `main.py`:

```python
from comet_sdkp.CDP4Adaptor import Cdp4SessionService

def main():
    # Create service instance
    service = Cdp4SessionService()
    
    # Connect to CDP4 server
    print("Connecting to CDP4 server...")
    result = service.open(
        "http://localhost:5000",
        "admin",
        "password"
    )
    
    if result is not None:
        print(f"Connection failed: {result}")
        return
    
    if not service.isSessionOpen:
        print("Session is not open")
        return
    
    print("✓ Connected successfully!")
    
    # Retrieve participant models
    print("\nRetrieving models...")
    models = service.getParticipantModels()
    
    if not models:
        print("No models found")
        return
    
    print(f"✓ Found {len(models)} model(s):\n")
    
    for i, model in enumerate(models, 1):
        print(f"  {i}. {model.Name}")
    
    # Get domains for first model
    if models:
        model = models[0]
        print(f"\nRetrieving domains for '{model.Name}'...")
        
        domains = service.getAvailableDomains(model)
        
        if domains:
            print(f"✓ Found {len(domains)} domain(s):\n")
            for i, domain in enumerate(domains, 1):
                print(f"  {i}. {domain.Name}")
        else:
            print("No domains found")

if __name__ == "__main__":
    main()
```

### Step 4: Run Your Script

```bash
python main.py
```

Expected output:
```
Connecting to CDP4 server...
✓ Connected successfully!

Retrieving models...
✓ Found 1 model(s):

  1. Test Model

Retrieving domains for 'Test Model'...
✓ Found 2 domain(s):

  1. Systems Engineering
  2. Thermal Engineering
```

## Working with Iterations

To open and work with iterations:

```python
from comet_sdkp.CDP4Adaptor import (
    Cdp4SessionService,
    computeProductTree,
)

service = Cdp4SessionService()

if service.open("http://localhost:5000", "admin", "password"):
    models = service.getParticipantModels()
    
    if models:
        model = models[0]
        domains = service.getAvailableDomains(model)
        
        if domains:
            # Open the active iteration
            iteration = service.openActiveIteration(model, domains[0])
            
            if iteration:
                print(f"Opened iteration: {iteration.Iid}")
                
                # Compute product tree
                if iteration.Option:
                    option = iteration.Option[0]
                    tree = computeProductTree(iteration, option)
                    
                    print(f"Product tree has {len(tree)} elements")
                    
                    for element in tree:
                        print(f"  - {element.Name}")
```

## Error Handling

Always include error handling:

```python
from comet_sdkp.CDP4Adaptor import Cdp4SessionService

service = Cdp4SessionService()

try:
    result = service.open("http://localhost:5000", "admin", "password")
    
    if result is not None:
        print(f"Connection error: {result}")
        exit(1)
    
    if not service.isSessionOpen:
        print("Failed to open session")
        exit(1)
    
    # Your code here
    models = service.getParticipantModels()
    print(f"Found {len(models)} models")
    
except Exception as e:
    print(f"Unexpected error: {e}")
    exit(1)
```

## Next Steps

- [API Reference](../api/index.md) - Learn about all available classes and functions
- [Examples](examples.md) - See more advanced examples
- [Troubleshooting](troubleshooting.md) - Fix common issues