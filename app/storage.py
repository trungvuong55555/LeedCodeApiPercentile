import threading
import bisect
from typing import Dict, List, Optional

pool_store: Dict[int, List[float]] = {}  # Dictionary storing pools
pool_lock = threading.Lock()  # Lock to ensure thread safety


def get_pool_values(pool_id: int) -> Optional[List[float]]:
    """Retrieve values from a pool if it exists."""
    with pool_lock:
        return pool_store.get(pool_id)


def append_to_pool(pool_id: int, values: List[float]) -> str:
    """Append values to a pool while maintaining sorted order for optimized quantile computation."""
    with pool_lock:
        if pool_id in pool_store:
            for value in values:
                bisect.insort(pool_store[pool_id], value)  # Insert values while maintaining sorted order
            return "appended"
        else:
            pool_store[pool_id] = sorted(values)  # Initialize pool with sorted values
            return "inserted"
