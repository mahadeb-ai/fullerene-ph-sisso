"""Canonical fullerene PH feature calculation, refactored from ``FeatTopo.py``."""

from __future__ import annotations
from pathlib import Path
from typing import Any
import numpy as np
import pandas as pd

from ph_sisso.descriptors import ORDERS, descriptor_block
from ph_sisso.ph.complexes import build_rips_complex, read_xyz

BETTI_FILTRATIONS = (1, 2, 3, 4, 5)
META_COLUMNS = (
    "ID", "Atoms", "Point_group", "Library_id", "Charge", "Distortion_E",
    "Formation_E", "Ionisation_potential", "Electron_affinity",
    "Electronegativity", "Band_gap", "Fermi_E",
)


def betti_at_threshold(intervals: np.ndarray, threshold: float) -> float:
    """Count intervals alive under the half-open convention ``birth <= t < death``."""
    intervals = np.asarray(intervals, dtype=float).reshape(-1, 2)
    if not intervals.size:
        return 0.0
    return float(np.sum((intervals[:, 0] <= threshold) & (threshold < intervals[:, 1])))


def compute_features(
    points: np.ndarray,
    max_edge_length: float = 8.0,
    max_dimension: int = 3,
    homology_coeff_field: int = 11,
    betti_filtrations: tuple[float, ...] = BETTI_FILTRATIONS,
) -> tuple[dict[str, float], dict[str, float]]:
    """Compute the 15 Betti samples and 72 lifetime/death PH statistics."""
    tree = build_rips_complex(points, max_edge_length, max_dimension, homology_coeff_field)
    betti: dict[str, float] = {}
    stats: dict[str, float] = {}
    for dimension in (0, 1, 2):
        intervals = np.asarray(tree.persistence_intervals_in_dimension(dimension), dtype=float).reshape(-1, 2)
        for threshold in betti_filtrations:
            label = int(threshold) if float(threshold).is_integer() else threshold
            betti[f"betti{dimension}_t{label}"] = betti_at_threshold(intervals, threshold)
        for scale, prefix in (("lifetime", "life_"), ("death", "death_")):
            block = descriptor_block(intervals, scale)
            stats.update({f"{prefix}b{dimension}_{key}": value for key, value in block.items()})
    return betti, stats


def compute_dataset(
    input_table: str | Path,
    xyz_directory: str | Path,
    output: str | Path,
    **parameters: Any,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compute canonical PH tables for every row, keyed by zero-padded source ID."""
    input_table, xyz_directory, output = Path(input_table), Path(xyz_directory), Path(output)
    frame = pd.read_csv(input_table, dtype={"ID": str}) if input_table.suffix.lower() == ".csv" else pd.read_excel(input_table, dtype={"ID": str})
    missing_meta = [name for name in META_COLUMNS if name not in frame]
    if missing_meta:
        raise KeyError(f"Missing metadata columns: {missing_meta}")
    betti_rows, statistic_rows = [], []
    for row in frame.itertuples(index=False):
        identifier = str(getattr(row, "ID")).strip().zfill(4)
        points = read_xyz(xyz_directory / f"{identifier}.xyz")
        betti, statistics = compute_features(points, **parameters)
        metadata = {name: getattr(row, name) for name in META_COLUMNS}
        betti_rows.append({**metadata, **betti})
        statistic_rows.append({**metadata, **statistics})
    betti_frame, statistics_frame = pd.DataFrame(betti_rows), pd.DataFrame(statistic_rows)
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.suffix.lower() == ".parquet":
        statistics_frame.to_parquet(output, index=False)
        betti_frame.to_parquet(output.with_name(f"{output.stem}_betti{output.suffix}"), index=False)
    elif output.suffix.lower() == ".xlsx":
        with pd.ExcelWriter(output) as writer:
            betti_frame.to_excel(writer, sheet_name="betti_curve_15", index=False)
            statistics_frame.to_excel(writer, sheet_name="ph_stats_36_life_death", index=False)
    else:
        raise ValueError("output must end in .parquet or .xlsx")
    return betti_frame, statistics_frame

