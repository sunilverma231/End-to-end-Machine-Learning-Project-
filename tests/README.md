# Test Suite

This directory contains automated tests for the Student Performance Predictor application.

## Running Tests Locally

```bash
# Install pytest
pip install pytest

# Run all tests
pytest tests/ -v

# Run with coverage
pip install pytest-cov
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_application.py -v
```

## Test Categories

### 1. Application Health Tests
- Flask app initialization
- Module imports
- Basic configuration

### 2. Prediction Pipeline Tests
- CustomData class functionality
- Data to DataFrame conversion
- Input validation

### 3. Artifact Tests
- Model file existence
- Preprocessor file existence

### 4. Configuration Tests
- Procfile validation
- Requirements.txt check
- WSGI configuration

### 5. Data Validation Tests
- Score range validation (0-100)
- Gender value validation
- Categorical input validation

## CI/CD Integration

These tests run automatically on every push via GitHub Actions:
- ✅ Linting with flake8
- ✅ Unit tests with pytest
- ✅ Deployment only if tests pass

## Adding New Tests

1. Create test file: `tests/test_<feature>.py`
2. Import pytest: `import pytest`
3. Create test class: `class Test<Feature>:`
4. Add test methods: `def test_<scenario>(self):`
5. Use assertions: `assert condition, "error message"`

Example:
```python
def test_new_feature(self):
    """Test description."""
    result = my_function()
    assert result == expected_value
```

## Current Coverage

Run `pytest tests/ --cov=src` to see coverage report.

Target: >80% code coverage for core modules.
