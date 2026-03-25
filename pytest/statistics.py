"""Statistical functions for learning pytest."""

from typing import List


def mean(data: List[float]) -> float:
    """Calculate the arithmetic mean of a list of numbers."""
    if not data:
        raise ValueError("Cannot calculate mean of empty list")
    return sum(data) / len(data)


def median(data: List[float]) -> float:
    """Calculate the median of a list of numbers."""
    if not data:
        raise ValueError("Cannot calculate median of empty list")

    sorted_data = sorted(data)
    n = len(sorted_data)

    if n % 2 == 1:
        return sorted_data[n // 2]
    else:
        return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2


def variance(data: List[float], ddof: int = 0) -> float:
    """Calculate the variance of a list of numbers.

    Args:
        data: List of numbers
        ddof: Delta degrees of freedom (0 for population, 1 for sample)
    """
    if not data:
        raise ValueError("Cannot calculate variance of empty list")
    if len(data) <= ddof:
        raise ValueError(f"Need at least {ddof + 1} data points")

    m = mean(data)
    return sum((x - m) ** 2 for x in data) / (len(data) - ddof)


def std(data: List[float], ddof: int = 0) -> float:
    """Calculate the standard deviation of a list of numbers.

    Args:
        data: List of numbers
        ddof: Delta degrees of freedom (0 for population, 1 for sample)
    """
    return variance(data, ddof) ** 0.5


def correlation(x: List[float], y: List[float]) -> float:
    """Calculate Pearson correlation coefficient between two lists."""
    if not x or not y:
        raise ValueError("Cannot calculate correlation of empty list")
    if len(x) != len(y):
        raise ValueError("Lists must have the same length")
    if len(x) < 2:
        raise ValueError("Need at least 2 data points")

    n = len(x)
    mean_x = mean(x)
    mean_y = mean(y)

    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator = (
        sum((xi - mean_x) ** 2 for xi in x) * sum((yi - mean_y) ** 2 for yi in y)
    ) ** 0.5

    if denominator == 0:
        raise ValueError("Cannot calculate correlation when all values are the same")

    return numerator / denominator
