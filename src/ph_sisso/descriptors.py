"""Persistent-homology descriptor definitions used by the manuscript.

Infinite-death intervals are excluded. Lifetimes are ``death - birth`` and only
strictly positive values are retained. Death-scale descriptors similarly retain
strictly positive death values. The historical implementation adds ``epsilon``
to normalization and logarithm denominators; this is preserved exactly. Negative
orders are therefore evaluated only after zero values have been removed.
"""

from __future__ import annotations

from collections.abc import Iterable
import numpy as np

EPSILON = 1.0e-12
ORDERS = (-2, -1, 1, 2, 3)


def finite_intervals(intervals: Iterable[Iterable[float]]) -> np.ndarray:
    """Return a validated ``(n, 2)`` array containing finite-death intervals."""
    array = np.asarray(list(intervals), dtype=float)
    if array.size == 0:
        return np.empty((0, 2), dtype=float)
    array = array.reshape(-1, 2)
    return array[np.isfinite(array[:, 1])]


def interval_values(intervals: Iterable[Iterable[float]], scale: str = "lifetime") -> np.ndarray:
    """Return positive lifetime or death-scale values from finite intervals."""
    finite = finite_intervals(intervals)
    if scale == "lifetime":
        values = finite[:, 1] - finite[:, 0]
    elif scale == "death":
        values = finite[:, 1]
    else:
        raise ValueError("scale must be 'lifetime' or 'death'")
    return values[values > 0.0]


def n_k(intervals: Iterable[Iterable[float]], scale: str = "lifetime") -> float:
    """Number of retained finite, positive interval values."""
    return float(interval_values(intervals, scale).size)


def ell_max(intervals: Iterable[Iterable[float]], scale: str = "lifetime") -> float:
    """Maximum retained lifetime or death value, or zero for an empty barcode."""
    values = interval_values(intervals, scale)
    return float(np.max(values)) if values.size else 0.0


def persistence_moment(
    intervals: Iterable[Iterable[float]], order: int, scale: str = "lifetime"
) -> float:
    """Mean of interval values raised to ``order`` (the original PH moment)."""
    values = interval_values(intervals, scale)
    return float(np.mean(values**order)) if values.size else 0.0


def generalized_persistence_entropy(
    intervals: Iterable[Iterable[float]],
    order: int,
    scale: str = "lifetime",
    epsilon: float = EPSILON,
) -> float:
    """Original order-weighted Shannon entropy used in the feature workbook.

    For positive retained values ``x_i``, weights are ``w_i=x_i**order`` and
    ``p_i=w_i/(sum(w)+epsilon)``; the result is
    ``-sum(p_i*log(p_i+epsilon))``. Invalid/non-positive weight sums return zero.
    """
    values = interval_values(intervals, scale)
    if not values.size:
        return 0.0
    weights = values**order
    total = float(np.sum(weights))
    if total <= epsilon or not np.isfinite(total):
        return 0.0
    probabilities = weights / (total + epsilon)
    return -float(np.sum(probabilities * np.log(probabilities + epsilon)))


def death_scale_entropy(intervals: Iterable[Iterable[float]], order: int) -> float:
    """Convenience wrapper for generalized entropy of positive death values."""
    return generalized_persistence_entropy(intervals, order, scale="death")


def descriptor_block(intervals: Iterable[Iterable[float]], scale: str) -> dict[str, float]:
    """Return the exact 12-value block used for one homology dimension."""
    result = {"N": n_k(intervals, scale), "ell_max": ell_max(intervals, scale)}
    result.update({f"H_r{r}": generalized_persistence_entropy(intervals, r, scale) for r in ORDERS})
    result.update({f"M_q{q}": persistence_moment(intervals, q, scale) for q in ORDERS})
    return result

