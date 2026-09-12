"""Reusable regression metrics with the manuscript prediction-minus-reference sign."""

from __future__ import annotations
from collections.abc import Iterable
import numpy as np


def regression_metrics(reference: Iterable[float], prediction: Iterable[float]) -> dict[str, float | int]:
    y, p = np.asarray(reference, dtype=float), np.asarray(prediction, dtype=float)
    valid = np.isfinite(y) & np.isfinite(p)
    y, p = y[valid], p[valid]
    if y.size == 0:
        raise ValueError("No finite reference/prediction pairs")
    error = p - y
    ss_res = float(np.sum(error**2))
    ss_tot = float(np.sum((y - np.mean(y))**2))
    return {
        "N_test": int(y.size),
        "R2": 1.0 - ss_res / ss_tot if ss_tot else float("nan"),
        "RMSE": float(np.sqrt(np.mean(error**2))),
        "MAE": float(np.mean(np.abs(error))),
        "mean_error": float(np.mean(error)),
        "median_absolute_error": float(np.median(np.abs(error))),
        "maximum_absolute_error": float(np.max(np.abs(error))),
    }

