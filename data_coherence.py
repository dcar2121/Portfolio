"""Data coherence utilities for network state measurements."""
from typing import Sequence, List
import numpy as np


def data_coherence_signal(data: Sequence[float]) -> List[float]:
    """Compute a simple running-coherence signal (running mean).

    This function is intentionally small and illustrative. In production,
    use streaming windows, robust statistics, and provenance metadata.
    """
    arr = np.asarray(data, dtype=float)
    if arr.size == 0:
        return []
    out = np.empty_like(arr)
    cumsum = 0.0
    for i, v in enumerate(arr):
        cumsum += v
        out[i] = cumsum / (i + 1)
    return out.tolist()


def example():
    data = [1, 2, 3, 4, 5]
    print(data_coherence_signal(data))


if __name__ == "__main__":
    example()
