"""Error handling tests - learning pytest.raises for exceptions."""

import pytest
import statistics


class TestMeanErrors:
    """Tests for mean function error handling."""

    def test_mean_empty_list(self):
        """Test that mean raises ValueError for empty list."""
        with pytest.raises(ValueError, match="empty list"):
            statistics.mean([])


class TestMedianErrors:
    """Tests for median function error handling."""

    def test_median_empty_list(self):
        """Test that median raises ValueError for empty list."""
        with pytest.raises(ValueError, match="empty list"):
            statistics.median([])


class TestVarianceErrors:
    """Tests for variance function error handling."""

    def test_variance_empty_list(self):
        """Test that variance raises ValueError for empty list."""
        with pytest.raises(ValueError, match="empty list"):
            statistics.variance([])

    def test_variance_single_element_population(self):
        """Test variance with ddof=0 and single element returns 0."""
        result = statistics.variance([5], ddof=0)
        assert result == 0.0

    def test_variance_insufficient_data_sample(self):
        """Test variance with ddof=1 but only 1 element."""
        with pytest.raises(ValueError, match="at least"):
            statistics.variance([5], ddof=1)


class TestCorrelationErrors:
    """Tests for correlation function error handling."""

    def test_correlation_empty_x(self):
        """Test correlation with empty x list."""
        with pytest.raises(ValueError, match="empty"):
            statistics.correlation([], [1, 2, 3])

    def test_correlation_empty_y(self):
        """Test correlation with empty y list."""
        with pytest.raises(ValueError, match="empty"):
            statistics.correlation([1, 2, 3], [])

    def test_correlation_mismatched_lengths(self):
        """Test correlation with mismatched list lengths."""
        with pytest.raises(ValueError, match="same length"):
            statistics.correlation([1, 2, 3], [1, 2])

    def test_correlation_single_point(self):
        """Test correlation with single data point."""
        with pytest.raises(ValueError, match="at least 2"):
            statistics.correlation([1], [2])

    def test_correlation_constant_values(self):
        """Test correlation with constant values (division by zero)."""
        with pytest.raises(ValueError, match="same"):
            statistics.correlation([1, 2, 3], [5, 5, 5])
