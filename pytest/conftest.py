"""Shared fixtures available to all tests - demonstrates conftest.py."""

import pytest


@pytest.fixture
def sample_numbers():
    """Basic sample data for testing."""
    return [10, 20, 30, 40, 50]


@pytest.fixture
def small_sample():
    """Small sample for basic tests."""
    return [1, 2, 3]


@pytest.fixture
def numbers_with_zeros():
    """Numbers including zeros."""
    return [0, 1, 2, 3, 0]


@pytest.fixture
def correlation_pairs():
    """Perfectly correlated data."""
    return [1, 2, 3, 4, 5], [2, 4, 6, 8, 10]


@pytest.fixture
def inverse_correlation_pairs():
    """Perfectly inversely correlated data."""
    return [1, 2, 3, 4, 5], [10, 8, 6, 4, 2]


@pytest.fixture
def setup_message():
    """Fixture with setup and teardown."""
    print("\n  [SETUP] Setting up test...")
    yield "test data"
    print("\n  [TEARDOWN] Cleaning up after test...")


@pytest.fixture(scope="session")
def session_data():
    """Session-scoped fixture - created once per test session."""
    return {"runs": 0}


@pytest.fixture
def increment_session(session_data):
    """Modifies and returns session-scoped data."""
    session_data["runs"] += 1
    return session_data
