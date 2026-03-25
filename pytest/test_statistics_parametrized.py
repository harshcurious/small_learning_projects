"""Parametrized tests for statistics module - learning pytest.mark.parametrize."""

import pytest
import statistics


class TestMeanParametrized:
    """Parametrized tests for mean function."""

    @pytest.mark.parametrize(
        "data,expected",
        [
            ([1, 2, 3, 4, 5], 3.0),
            ([10, 20, 30], 20.0),
            ([-2, 0, 2], 0.0),
            ([0.5, 1.5, 2.5], 1.5),
            ([100], 100.0),
            ([0, 0, 0], 0.0),
        ],
    )
    def test_mean_values(self, data, expected):
        """Test mean with various input data."""
        assert statistics.mean(data) == expected


class TestMedianParametrized:
    """Parametrized tests for median function."""

    @pytest.mark.parametrize(
        "data,expected",
        [
            ([1, 2, 3], 2),
            ([1, 2, 3, 4], 2.5),
            ([3, 1, 2], 2),
            ([5], 5),
            ([1, 1, 1], 1),
            ([-3, -1, 0, 1, 3], 0),
        ],
    )
    def test_median_values(self, data, expected):
        """Test median with various input data."""
        assert statistics.median(data) == expected


class TestVarianceParametrized:
    """Parametrized tests for variance function."""

    @pytest.mark.parametrize(
        "data,ddof,expected",
        [
            ([1, 2, 3, 4, 5], 0, 2.0),
            ([1, 2, 3, 4, 5], 1, 2.5),
            ([2, 4, 4, 4, 5, 5, 7, 9], 0, 4.0),
            ([2, 4, 4, 4, 5, 5, 7, 9], 1, 4.571428571428571),
            ([10, 10, 10], 0, 0.0),
        ],
    )
    def test_variance_values(self, data, ddof, expected):
        """Test variance with various input data."""
        assert statistics.variance(data, ddof=ddof) == expected


class TestCorrelationParametrized:
    """Parametrized tests for correlation function."""

    @pytest.mark.parametrize(
        "x,y,expected",
        [
            ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], 1.0),
            ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], -1.0),
            ([1, 2, 3], [1, 2, 3], 1.0),
            ([1, 2, 3], [3, 2, 1], -1.0),
        ],
    )
    def test_correlation_values(self, x, y, expected):
        """Test correlation with various input data."""
        assert statistics.correlation(x, y) == expected
