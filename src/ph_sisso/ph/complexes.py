"""XYZ input and Vietoris--Rips complex construction."""

from __future__ import annotations
from pathlib import Path
import numpy as np


def read_xyz(path: str | Path) -> np.ndarray:
    """Read Cartesian coordinates (Angstrom) from a conventional XYZ file."""
    path = Path(path)
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) < 3:
        raise ValueError(f"XYZ file is too short: {path}")
    try:
        declared = int(lines[0].strip())
    except ValueError as exc:
        raise ValueError(f"Invalid XYZ atom count: {path}") from exc
    coordinates: list[list[float]] = []
    for line in lines[2:]:
        fields = line.split()
        if len(fields) >= 4:
            coordinates.append([float(fields[1]), float(fields[2]), float(fields[3])])
    array = np.asarray(coordinates, dtype=float)
    if array.shape != (declared, 3):
        raise ValueError(f"Expected {declared} coordinates in {path}, found {len(array)}")
    if not np.isfinite(array).all():
        raise ValueError(f"Non-finite coordinate in {path}")
    return array


def build_rips_complex(
    points: np.ndarray,
    max_edge_length: float = 8.0,
    max_dimension: int = 3,
    homology_coeff_field: int = 11,
):
    """Build and persist the manuscript GUDHI Rips simplex tree."""
    import gudhi

    points = np.asarray(points, dtype=float)
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("points must have shape (n_atoms, 3)")
    tree = gudhi.RipsComplex(points=points, max_edge_length=max_edge_length).create_simplex_tree(
        max_dimension=max_dimension
    )
    tree.persistence(homology_coeff_field=homology_coeff_field)
    return tree

