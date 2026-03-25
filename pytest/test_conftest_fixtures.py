"""Tests using shared fixtures from conftest.py."""

import statistics


def test_mean_with_sample(sample_numbers):
    """Use shared sample_numbers fixture."""
    assert statistics.mean(sample_numbers) == 30.0


def test_median_with_small(small_sample):
    """Use shared small_sample fixture."""
    assert statistics.median(small_sample) == 2


def test_mean_with_zeros(numbers_with_zeros):
    """Use shared numbers_with_zeros fixture."""
    assert statistics.mean(numbers_with_zeros) == 1.2


def test_correlation_shared(correlation_pairs):
    """Use shared correlation_pairs fixture."""
    x, y = correlation_pairs
    assert statistics.correlation(x, y) == 1.0


def test_inverse_correlation(inverse_correlation_pairs):
    """Use shared inverse_correlation_pairs fixture."""
    x, y = inverse_correlation_pairs
    assert statistics.correlation(x, y) == -1.0


def test_setup_teardown(setup_message):
    """Demonstrate setup/teardown with fixture."""
    assert setup_message == "test data"


def test_session_fixture_1(increment_session):
    """Test session fixture - first run."""
    assert increment_session["runs"] == 1


def test_session_fixture_2(increment_session):
    """Test session fixture - second run."""
    assert increment_session["runs"] == 2


def test_session_fixture_3(increment_session):
    """Test session fixture - third run."""
    assert increment_session["runs"] == 3
