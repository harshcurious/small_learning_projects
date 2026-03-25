"""Fixtures tests - learning pytest fixtures with setup/teardown."""

import pytest
import statistics


@pytest.fixture
def simple_data():
    """Simple list of numbers for testing."""
    return [1, 2, 3, 4, 5]


@pytest.fixture
def negative_data():
    """List with negative numbers."""
    return [-5, -3, -1, 0, 1, 3, 5]


@pytest.fixture
def float_data():
    """List of float values."""
    return [1.5, 2.5, 3.0, 4.5, 5.5]


@pytest.fixture
def large_dataset():
    """Larger dataset for more realistic testing."""
    return list(range(1, 101))


@pytest.fixture
def paired_data():
    """Two related lists for correlation testing."""
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    return x, y


class TestFixtures:
    """Tests demonstrating use of fixtures."""

    def test_mean_with_simple_data(self, simple_data):
        """Test mean using simple_data fixture."""
        assert statistics.mean(simple_data) == 3.0

    def test_median_with_simple_data(self, simple_data):
        """Test median using simple_data fixture."""
        assert statistics.median(simple_data) == 3

    def test_mean_with_negative_data(self, negative_data):
        """Test mean using negative_data fixture."""
        assert statistics.mean(negative_data) == 0.0

    def test_median_with_negative_data(self, negative_data):
        """Test median using negative_data fixture."""
        assert statistics.median(negative_data) == 0

    def test_mean_with_float_data(self, float_data):
        """Test mean using float_data fixture."""
        assert statistics.mean(float_data) == 3.4

    def test_variance_with_large_dataset(self, large_dataset):
        """Test variance using large_dataset fixture."""
        result = statistics.variance(large_dataset, ddof=1)
        assert abs(result - 841.67) < 0.01

    def test_correlation_with_paired_data(self, paired_data):
        """Test correlation using paired_data fixture."""
        x, y = paired_data
        assert statistics.correlation(x, y) == 1.0


class TestFixturesScoped:
    """Demonstrating session-scoped fixtures."""

    def test_first_use(self, large_dataset):
        """First use of large_dataset."""
        assert len(large_dataset) == 100

    def test_second_use(self, large_dataset):
        """Second use of large_dataset - same fixture."""
        assert statistics.mean(large_dataset) == 50.5
