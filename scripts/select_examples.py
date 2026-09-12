#!/usr/bin/env python3
"""Reproduce the pre-validated representative held-out examples by fixed ID."""

from __future__ import annotations
import argparse, sys
from pathlib import Path
import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from ph_sisso.equations import distortion_main, distortion_supplementary, fermi_main, fermi_supplementary
from ph_sisso.io import load_sources
from ph_sisso.splits import load_manifest

DISTORTION = [(32, "small", "1/3"), (4985, "small", "2/3"), (360, "intermediate", "1/3"), (5806, "intermediate", "2/3"), (2283, "large", "1/3"), (7033, "large", "2/3")]
FERMI = [(1665, -1, "25%"), (955, -1, "50%"), (401, -1, "75%"), (2916, 1, "25%"), (3700, 1, "50%"), (4169, 1, "75%")]


def select(data: pd.DataFrame, dm: pd.DataFrame, fm: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for identifier, branch, quantile in DISTORTION:
        if not ((dm.ID == identifier) & (dm.split == "test") & (dm.branch == branch)).any(): raise AssertionError(f"ID {identifier} is not in distortion test branch {branch}")
        frame = data[data.ID == identifier]
        main, supp = distortion_main(frame, branch)[0], distortion_supplementary(frame, branch)[0]
        rows.append({"target": "Distortion_E", "ID": identifier, "Atoms": int(frame.Atoms.iloc[0]), "Charge": int(frame.Charge.iloc[0]), "branch": branch, "selection_quantile": quantile, "reference": float(frame.Distortion_E.iloc[0]), "main_prediction": main, "supplementary_prediction": supp, "main_absolute_error": abs(main-float(frame.Distortion_E.iloc[0])), "supplementary_absolute_error": abs(supp-float(frame.Distortion_E.iloc[0]))})
    for identifier, charge, quantile in FERMI:
        branch = f"Q_{charge:+d}"
        if not ((fm.ID == identifier) & (fm.split == "test") & (fm.branch == branch)).any(): raise AssertionError(f"ID {identifier} is not in Fermi test branch {branch}")
        frame = data[data.ID == identifier]
        main, supp = fermi_main(frame, charge)[0], fermi_supplementary(frame, charge)[0]
        rows.append({"target": "Fermi_E", "ID": identifier, "Atoms": int(frame.Atoms.iloc[0]), "Charge": charge, "branch": branch, "selection_quantile": quantile, "reference": float(frame.Fermi_E.iloc[0]), "main_prediction": main, "supplementary_prediction": supp, "main_absolute_error": abs(main-float(frame.Fermi_E.iloc[0])), "supplementary_absolute_error": abs(supp-float(frame.Fermi_E.iloc[0]))})
    return pd.DataFrame(rows)


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--config", type=Path, default=ROOT / "configs/manuscript.yaml"); parser.add_argument("--targets", type=Path); parser.add_argument("--ph-features", type=Path); args = parser.parse_args()
    config = yaml.safe_load(args.config.read_text()); resolve = lambda x: (ROOT / x).resolve()
    data = load_sources(args.targets or resolve(config["targets"]), args.ph_features or resolve(config["ph_features"]), config.get("ph_sheet", "ph_stats_36_life_death"))
    result = select(data, load_manifest(resolve(config["distortion_manifest"])), load_manifest(resolve(config["fermi_manifest"])))
    output = resolve(config["output_directory"]) / "tables"; output.mkdir(parents=True, exist_ok=True); result.to_csv(output / "representative_examples.csv", index=False)
    print(result.to_string(index=False)); return 0


if __name__ == "__main__": raise SystemExit(main())

