"""Target-specific split manifests; there is deliberately no universal split."""

from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd


MANIFEST_COLUMNS = ["target", "model_variant", "branch", "ID", "Atoms", "Charge", "split", "seed", "split_method", "source_sha256"]


def load_manifest(path: str | Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    missing = [name for name in MANIFEST_COLUMNS if name not in frame]
    if missing:
        raise ValueError(f"Manifest lacks columns: {missing}")
    if frame.duplicated(["target", "model_variant", "ID"]).any():
        raise ValueError("Duplicate target/model/ID assignment")
    return frame


def deterministic_random_split(ids: list[int], test_fraction: float = 0.2, seed: int = 42) -> dict[int, str]:
    """Small deterministic split helper for tests/robustness, not canonical reconstruction."""
    ordered = np.asarray(sorted(ids), dtype=int)
    rng = np.random.RandomState(seed)
    permutation = rng.permutation(ordered)
    n_test = int(np.ceil(len(ordered) * test_fraction))
    test = set(permutation[:n_test])
    return {int(identifier): ("test" if identifier in test else "train") for identifier in ordered}


def subset_from_manifest(data: pd.DataFrame, manifest: pd.DataFrame, split: str = "test") -> pd.DataFrame:
    selected = manifest.loc[manifest["split"].eq(split), "ID"].astype(int)
    result = data[data["ID"].isin(selected)].copy()
    if len(result) != len(selected):
        raise ValueError("Manifest IDs do not map one-to-one to source data")
    return result.sort_values("ID", kind="stable").reset_index(drop=True)

