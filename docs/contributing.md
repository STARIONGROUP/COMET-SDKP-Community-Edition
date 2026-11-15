# Contributing Guide

We welcome contributions to COMET SDKP! This guide will help you get started.

## How to Contribute

### Report Bugs

1. Check [GitHub Issues](https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition/issues) to avoid duplicates
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs. actual behavior
   - Environment info (Python, OS, SDK version)
   - Stack trace (if applicable)

### Suggest Features

1. Open a GitHub Discussion or Issue
2. Describe the feature and use case
3. Provide examples of how it would be used
4. Discuss implementation approach

### Submit Code Changes

#### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/STARIONGROUP/COMET-SDKP-Community-Edition.git
cd COMET-SDKP-Community-Edition

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

#### Make Your Changes

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Write tests for new functionality
4. Update documentation

#### Run Tests

```bash
# All tests
pytest tests/ -v

# Unit tests only
pytest tests/unit/ -v

# With coverage
pytest tests/ --cov=comet_sdkp

# Live tests (require a CDP4-COMET server, see below)
pytest tests/live/ -v
```

#### Code Style

- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Write docstrings for all functions

#### Submit Pull Request

1. Push to your fork: `git push origin feature/your-feature-name`
2. Create a Pull Request on GitHub
3. Provide clear description of changes
4. Link related issues
5. Ensure all tests pass

## Development Workflow

### Project Structure

```
COMET-SDKP-Community-Edition/
├── src/
│   └── comet_sdkp/       # Main package
│       ├── CDP4Adaptor.py
│       ├── __init__.py
│       └── libs/         # .NET libraries of the CDP4-COMET SDK
├── tests/                # Test suite
│   ├── unit/
│   ├── integration/
│   ├── smoke/
│   ├── live/             # Tests against a real server
│   └── ...
├── docs/                 # Documentation
│   ├── guides/
│   ├── api/
│   ├── _build/
│   └── ...
├── pyproject.toml        # Package, test and tool configuration
└── README.md
```

### Running Tests Locally

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_CDP4Adaptor.py

# Run specific test
pytest tests/unit/test_CDP4Adaptor.py::TestCdp4SessionServiceOpen::test_open_with_valid_parameters

# Run with coverage
pytest --cov=comet_sdkp --cov-report=html

# Run only the tests of one kind, by marker
pytest -m unit
pytest -m integration
pytest -m smoke
```

Each test gets the marker of its directory under `tests/` (`unit`, `integration`, `smoke` or `live`).
The pytest configuration is in `pyproject.toml`; it measures coverage on every run and writes an
HTML report to `coverage_html/`. Pass `--no-cov` to switch that off.

### Running the Live Tests

The unit, integration and smoke tests replace the .NET libraries with mocks and need no server.
The tests in `tests/live/` use the real libraries and a running CDP4-COMET server. They are skipped
unless these environment variables are set:

```bash
export COMET_TEST_SERVER_URL=http://localhost:5000
export COMET_TEST_USERNAME=admin
export COMET_TEST_PASSWORD=pass

pytest tests/live/ -v
```

On Windows PowerShell, use `$env:COMET_TEST_SERVER_URL = "http://localhost:5000"` and so on.

### Building Documentation

```bash
# Install doc dependencies
pip install -e ".[docs]"

# Build HTML docs
cd docs
make html

# View in browser
open _build/html/index.html  # macOS
start _build/html/index.html  # Windows
xdg-open _build/html/index.html  # Linux
```

## Code Standards

### Type Hints

Always use type hints:

```python
def open(self, uri: str, username: str, password: str) -> str | None:
    """Open a connection to CDP4 server."""
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def computeProductTree(iteration: Iteration, option: Option) -> list[NestedElement]:
    """Generate a nested element tree.
    
    Args:
        iteration: The iteration to compute from
        option: The option for which to compute the tree
        
    Returns:
        List of nested element objects
        
    Raises:
        ValueError: If iteration or option not provided
    """
    ...
```

### Testing

Write tests for all new functionality:

```python
class TestNewFeature:
    """Tests for new feature"""
    
    def test_basic_functionality(self):
        """Test that feature works correctly"""
        result = new_function()
        assert result is not None
    
    def test_error_handling(self):
        """Test error cases"""
        with pytest.raises(ValueError):
            new_function(None)
```

## Review Process

1. **Checks**: Run the tests and the code quality tools locally before you submit
2. **Code Review**: Maintainers review your code
3. **Revisions**: Make requested changes
4. **Approval**: Code is approved and merged

## Release Process

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes

Releases are made when enough features/fixes accumulate, typically monthly.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Respect different opinions
- Help others learn and grow

## Questions?

- 💬 Open a GitHub Discussion
- 📧 Contact maintainers
- 📖 Check documentation

Thank you for contributing!