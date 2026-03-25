"""Tests with markers - learning pytest markers and CLI options."""

import pytest
import statistics


@pytest.mark.basic
def test_mean_basic():
    """Basic test - marked with @pytest.mark.basic."""
    assert statistics.mean([1, 2, 3]) == 2.0


@pytest.mark.basic
def test_median_basic():
    """Basic test - marked with @pytest.mark.basic."""
    assert statistics.median([1, 2, 3]) == 2


@pytest.mark.slow
@pytest.mark.skip(reason="Demonstrating skip marker")
def test_skipped_demo():
    """This test is skipped to demonstrate skip marker."""
    assert False


@pytest.mark.slow
def test_variance_large():
    """Slow test - marked with @pytest.mark.slow."""
    data = list(range(10000))
    result = statistics.variance(data, ddof=1)
    assert result > 0


@pytest.mark.unit
class TestUnit:
    """Unit tests marked with @pytest.mark.unit."""

    def test_mean_unit(self):
        assert statistics.mean([5, 10, 15]) == 10.0

    def test_median_unit(self):
        assert statistics.median([5, 10, 15]) == 10


@pytest.mark.integration
class TestIntegration:
    """Integration tests marked with @pytest.mark.integration."""

    def test_mean_median_combo(self):
        data = [1, 2, 3, 4, 5]
        m = statistics.mean(data)
        med = statistics.median(data)
        assert m == 3.0
        assert med == 3

    def test_all_stats(self):
        data = [1, 2, 3, 4, 5]
        assert statistics.mean(data) == 3.0
        assert statistics.median(data) == 3
        var = statistics.variance(data, ddof=1)
        std = statistics.std(data, ddof=1)
        assert abs(std**2 - var) < 0.0001


@pytest.mark.parametrize("n", [1, 10, 100, 1000])
@pytest.mark.slow
def test_mean_performance(n):
    """Parametrized performance test."""
    data = list(range(n))
    result = statistics.mean(data)
    expected = (n - 1) / 2
    assert abs(result - expected) < 0.001
