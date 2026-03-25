"""Basic pytest tests for statistics module."""

import stats as statistics


def test_mean_simple():
    """Test mean with a simple list of numbers."""
    result = statistics.mean([1, 2, 3, 4, 5])
    assert result == 3.0


def test_mean_single_value():
    """Test mean with a single value."""
    result = statistics.mean([42])
    assert result == 42.0


def test_mean_negative_numbers():
    """Test mean with negative numbers."""
    result = statistics.mean([-3, -1, 1, 3])
    assert result == 0.0


def test_mean_floats():
    """Test mean with float values."""
    result = statistics.mean([1.5, 2.5, 3.0])
    assert result == 2.3333333333333335


def test_median_odd_length():
    """Test median with odd number of elements."""
    result = statistics.median([1, 3, 2])
    assert result == 2


def test_median_even_length():
    """Test median with even number of elements."""
    result = statistics.median([1, 2, 3, 4])
    assert result == 2.5


def test_median_single_value():
    """Test median with single value."""
    result = statistics.median([5])
    assert result == 5


def test_median_negative():
    """Test median with negative numbers."""
    result = statistics.median([-5, -2, 0, 3, 8])
    assert result == 0


def test_variance_population():
    """Test population variance."""
    result = statistics.variance([2, 4, 4, 4, 5, 5, 7, 9], ddof=0)
    assert result == 4.0


def test_variance_sample():
    """Test sample variance."""
    result = statistics.variance([2, 4, 4, 4, 5, 5, 7, 9], ddof=1)
    assert result == 4.571428571428571


def test_std_population():
    """Test population standard deviation."""
    result = statistics.std([2, 4, 4, 4, 5, 5, 7, 9], ddof=0)
    assert result == 2.0


def test_correlation_perfect_positive():
    """Test correlation with perfect positive relationship."""
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]
    result = statistics.correlation(x, y)
    assert result == 1.0


def test_correlation_perfect_negative():
    """Test correlation with perfect negative relationship."""
    x = [1, 2, 3, 4, 5]
    y = [10, 8, 6, 4, 2]
    result = statistics.correlation(x, y)
    assert result == -1.0


def test_correlation_no_relationship():
    """Test correlation with weak linear relationship."""
    x = [1, 2, 3, 4, 5]
    y = [1, 3, 2, 5, 4]
    result = statistics.correlation(x, y)
    assert result > 0
