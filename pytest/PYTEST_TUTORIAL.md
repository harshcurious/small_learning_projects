# Pytest Tutorial

A quick reference guide for the pytest testing framework.

---

## Pytest Overview

Pytest discovers and runs tests automatically. It finds files named `test_*.py` and functions starting with `test_`.

---

## Your Test Files Explained

### 1. Basic Tests (`test_statistics.py`)

```python
def test_mean_simple():
    result = statistics.mean([1, 2, 3, 4, 5])
    assert result == 3.0
```

**Key concepts:**
- Test functions start with `test_`
- `assert` checks if condition is True — pytest shows what failed if not
- Tests are independent (run in any order)

---

### 2. Parametrized Tests (`test_statistics_parametrized.py`)

```python
@pytest.mark.parametrize("data,expected", [
    ([1, 2, 3, 4, 5], 3.0),
    ([10, 20, 30], 20.0),
])
def test_mean_values(self, data, expected):
    assert statistics.mean(data) == expected
```

**Key concepts:**
- `@pytest.mark.parametrize` runs the same test with different inputs
- Arguments come from the parametrize list
- Great for covering edge cases without writing multiple tests

---

### 3. Exception Testing (`test_statistics_errors.py`)

```python
def test_mean_empty_list():
    with pytest.raises(ValueError, match="empty list"):
        statistics.mean([])
```

**Key concepts:**
- `pytest.raises()` catches exceptions
- `match="text"` checks the error message
- Use this to test error handling code

---

### 4. Fixtures (`test_statistics_fixtures.py`)

```python
@pytest.fixture
def simple_data():
    return [1, 2, 3, 4, 5]

def test_mean_with_simple_data(self, simple_data):
    assert statistics.mean(simple_data) == 3.0
```

**Key concepts:**
- `@pytest.fixture` creates reusable test data
- Fixtures are injected as function arguments
- Run setup code before and cleanup after with `yield`

### Fixture Scope

```python
@pytest.fixture              # function scope (default) - created per test
@pytest.fixture(scope="class")  # class scope - created once per test class
@pytest.fixture(scope="module") # module scope - created once per file
@pytest.fixture(scope="session") # session scope - created once per test session
```

### Fixture with Teardown

```python
@pytest.fixture
def setup_and_teardown():
    print("Setup code runs here")
    yield "test data"
    print("Teardown code runs after test")
```

---

### 5. Shared Fixtures (`conftest.py`)

Put fixtures in `conftest.py` and they're available to **all test files** automatically.

```python
@pytest.fixture
def sample_numbers():
    return [10, 20, 30, 40, 50]
```

No imports needed — pytest finds them.

---

### 6. Markers (`test_statistics_markers.py`)

```python
@pytest.mark.slow
def test_variance_large():
    data = list(range(10000))
    result = statistics.variance(data, ddof=1)
    assert result > 0

@pytest.mark.skip(reason="Demonstrating skip marker")
def test_skipped_demo():
    ...
```

**Key concepts:**
- Markers label tests (slow, unit, integration, etc.)
- Run specific markers: `pytest -m "slow"`
- Skip tests with `@pytest.mark.skip`
- Register markers in `pytest.ini` to avoid warnings

**Common built-in markers:**
- `@pytest.mark.skip` - Skip a test
- `@pytest.mark.skipif(condition, reason)` - Skip if condition is true
- `@pytest.mark.xfail` - Expect test to fail
- `@pytest.mark.parametrize` - Run with multiple inputs

---

## Common CLI Options

| Command | What it does |
|---------|--------------|
| `pytest` | Run all tests |
| `pytest -v` | Verbose (show test names) |
| `pytest -q` | Quiet (less output) |
| `pytest -m "slow"` | Run only tests marked "slow" |
| `pytest -k "mean"` | Run tests with "mean" in name |
| `pytest --collect-only` | List tests without running |
| `pytest -x` | Stop on first failure |
| `pytest --tb=short` | Shorter traceback |
| `pytest -s` | Show print statements |
| `pytest --lf` | Run only tests that failed last time |

---

## Test Structure Best Practices

```
test_*.py          # Test files
Test*              # Test classes (optional)
test_*()           # Test functions
```

- One assertion per test is fine, but multiple related assertions are okay too
- Use descriptive names: `test_mean_of_empty_list_raises_error()` not `test1()`
- Fixtures for shared data, parametrization for variant inputs

---

## Configuration (`pytest.ini`)

```ini
[pytest]
markers =
    basic: Basic functionality tests
    slow: Tests that take longer to run
    unit: Unit tests
    integration: Integration tests

addopts = -v
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

---

## Files in This Project

| File | Purpose |
|------|---------|
| `statistics.py` | Sample module with mean, median, variance, std, correlation |
| `test_statistics.py` | Basic tests with simple assertions |
| `test_statistics_parametrized.py` | Tests using `@pytest.mark.parametrize` |
| `test_statistics_errors.py` | Tests using `pytest.raises` for exception handling |
| `test_statistics_fixtures.py` | Tests using local `@pytest.fixture` |
| `conftest.py` | Shared fixtures available to all tests |
| `test_statistics_markers.py` | Tests with `@pytest.mark` decorators |
| `pytest.ini` | Configuration file with custom markers |

---

## Running Tests

```bash
# Activate virtual environment
source .venv/bin/activate
# or
. .venv/bin/activate

# Run all tests
pytest

# Run specific file
pytest test_statistics.py

# Run with verbose output
pytest -v

# Run by marker
pytest -m "unit"

# Run by name pattern
pytest -k "mean"

# Show print statements
pytest -s

# Stop on first failure
pytest -x
```
