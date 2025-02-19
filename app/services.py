import numpy as np
from typing import List


def compute_quantile(values: List[float], percentile: float) -> float:
    """Compute the quantile:
    - If the pool has >= 100 values → Use NumPy for optimized computation.
    - If the pool has < 100 values → Use manual interpolation.
    """
    if not values:
        raise ValueError("Pool is empty, cannot compute quantile")

    if len(values) >= 100:
        return float(np.percentile(values, percentile))  # Use NumPy for large pools

    # Manual calculation for pools with < 100 values
    index = (percentile / 100) * (len(values) - 1)
    lower = int(index)
    upper = min(lower + 1, len(values) - 1)
    weight = index - lower

    return values[lower] * (1 - weight) + values[upper] * weight

