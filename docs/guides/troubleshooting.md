# Troubleshooting Guide

## Connection Issues

### Error: "The remote name could not be resolved"

**Symptom:**
```
The remote name could not be resolved: 'localhost'
```

**Solution:**
1. Check the server URL is correct
2. Verify the server is running
3. Check your network connection
4. Try using the IP address instead of hostname: `http://127.0.0.1:5000`

### Error: "No connection could be made"

**Symptom:**
```
No connection could be made because the target machine actively refused it
```

**Solution:**
1. Verify the CDP4 server is running
2. Check the correct port number (default: 5000)
3. Ensure firewall is not blocking the connection
4. Check that the server has the correct URL scheme (http vs https)

### Error: "Authentication failed"

**Symptom:**
```
Invalid username or password
```

**Solution:**
1. Verify username and password are correct
2. Check username case sensitivity
3. Ensure the user account is active in CDP4
4. Check user permissions in CDP4

## Import Errors

### Error: "No module named 'clr'"

**Symptom:**
```
ModuleNotFoundError: No module named 'clr'
```

**Solution:**
```bash
# Reinstall pythonnet
pip install --force-reinstall pythonnet>=3.0.5
```

### Error: "No module named 'comet_sdkp'"

**Symptom:**
```
ModuleNotFoundError: No module named 'comet_sdkp'
```

**Solution:**
```bash
# Install the SDK
pip install comet-sdkp

# Or from source
cd COMET-SDKP-Community-Edition
pip install -e .
```

## Session Issues

### Error: "Session already open"

**Cause:** You're trying to open a session that's already open

**Solution:**
```python
# Close existing session first
if service.isSessionOpen:
    service.isSessionOpen = False
    service.session = None

# Then open new session
service.open(url, username, password)
```

### Error: "No models found"

**Cause:** 
- No models are assigned to your user account
- The CDP4 server has no models defined
- Permission issue

**Solution:**
1. Check in CDP4 that models exist
2. Verify your user has access to the models
3. Contact your CDP4 administrator

### Error: "Failed to open Iteration"

**Cause:**
- Iteration doesn't exist
- Domain doesn't have access
- Iteration is frozen (read-only)

**Solution:**
1. Check iteration exists and is active
2. Verify domain has correct permissions
3. Check if iteration is frozen in CDP4

## Performance Issues

### Slow Product Tree Computation

**Solution:**
- Compute tree once and reuse it
- Filter elements early
- Process in batches

```python
# Good - filter first
tree = computeProductTree(iteration, option)
mass_elements = getElementByParameterType(tree, "Mass")

# Bad - iterate all then filter
for element in tree:
    if has_mass_parameter(element):
        process(element)
```

### Memory Usage Too High

**Solution:**
- Clear unused variables
- Process data in chunks
- Close sessions when done

```python
# Release memory
del large_list
service.isSessionOpen = False
service.session = None
```

## Type Errors in Tests

### Error: "MagicMock value cannot be converted to CDP4Common..."

**Cause:** Using mock objects where CDP4 expects real types

**Solution:**
Use `pytest.skip()` for tests that require real objects:

```python
def test_real_iteration():
    try:
        iteration = service.openActiveIteration(model, domain)
    except TypeError:
        pytest.skip("Cannot test with mocks - requires real CDP4 objects")
```

## Common Patterns

### Checking Session State

```python
if service.isSessionOpen:
    # Safe to use service
    models = service.getParticipantModels()
else:
    print("Session is not open")
```

### Safe Resource Cleanup

```python
try:
    service.open(url, user, password)
    # Do work
finally:
    if service.isSessionOpen:
        service.isSessionOpen = False
        service.session = None
```

### Handling Multiple Errors

```python
try:
    service.open(url, user, password)
except Exception as e:
    if "resolved" in str(e):
        print("Server not found")
    elif "refused" in str(e):
        print("Server is not running")
    elif "Authentication" in str(e):
        print("Invalid credentials")
    else:
        print(f"Unknown error: {e}")
```

## Getting Help

If you can't find a solution:

1. **Check the FAQ** - [FAQ Guide](faq.md)
2. **Search GitHub Issues** - [GitHub Issues](https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition/issues)
3. **Create a GitHub Issue** with:
   - Error message and full stack trace
   - Steps to reproduce
   - Your environment (Python version, OS, SDK version)
   - What you expected vs. what happened

4. **Check CDP4 Documentation** - [CDP4 Project](https://github.com/STARIONGROUP/CDP4-COMET)