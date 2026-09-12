"""Portable data loading, validation, and hashing utilities."""

from __future__ import annotations
import hashlib
from pathlib import Path
import pandas as pd

META = ["ID", "Atoms", "Point_group", "Library_id", "Charge", "Distortion_E", "Formation_E", "Ionisation_potential", "Electron_affinity", "Electronegativity", "Band_gap", "Fermi_E"]


def sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_sources(target_csv: str | Path, ph_table: str | Path, sheet: str = "ph_stats_36_life_death") -> pd.DataFrame:
    """Join target and PH sources one-to-one using exact ID and verify semantics."""
    targets = pd.read_csv(target_csv, low_memory=False)
    path = Path(ph_table)
    ph = pd.read_parquet(path) if path.suffix == ".parquet" else pd.read_excel(path, sheet_name=sheet, engine="openpyxl")
    for frame in (targets, ph):
        frame.columns = [str(column).strip() for column in frame.columns]
    if targets["ID"].duplicated().any() or ph["ID"].duplicated().any():
        raise ValueError("ID must be unique in both source tables")
    if set(targets["ID"]) != set(ph["ID"]):
        raise ValueError("Target and PH tables contain different IDs")
    feature_columns = [name for name in ph if name.startswith(("life_", "death_"))]
    merged = targets[META].merge(ph[["ID", *META[1:], *feature_columns]], on="ID", validate="one_to_one", suffixes=("_target", "_ph"))
    output = pd.DataFrame({name: merged[name] if name == "ID" else merged[f"{name}_target"] for name in META})
    for name in feature_columns:
        output[name] = merged[name]
    for name in ("Atoms", "Charge", "Distortion_E", "Formation_E", "Fermi_E"):
        left = pd.to_numeric(merged[f"{name}_target"], errors="coerce")
        right = pd.to_numeric(merged[f"{name}_ph"], errors="coerce")
        if not ((left == right) | (left.isna() & right.isna())).all():
            raise ValueError(f"Source mismatch for {name}")
    output["ID"] = pd.to_numeric(output["ID"]).astype(int)
    output["Atoms"] = pd.to_numeric(output["Atoms"]).astype(int)
    output["Charge"] = pd.to_numeric(output["Charge"]).astype(int)
    return output.sort_values("ID", kind="stable").reset_index(drop=True)

