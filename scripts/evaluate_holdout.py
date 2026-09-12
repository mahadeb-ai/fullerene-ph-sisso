#!/usr/bin/env python3
"""Evaluate fixed manuscript equations on immutable held-out manifests; never fit."""

from __future__ import annotations
import argparse
import sys
from pathlib import Path
import pandas as pd
import yaml

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY / "src"))

from ph_sisso.equations import distortion_main, distortion_supplementary, fermi_main, fermi_supplementary
from ph_sisso.io import load_sources
from ph_sisso.metrics import regression_metrics
from ph_sisso.splits import load_manifest, subset_from_manifest

REPORTED = {
    "distortion_main_small": (0.969, 1.012), "distortion_main_intermediate": (0.936, 1.284),
    "distortion_main_large": (0.961, 1.380), "distortion_supp_small": (0.9522, 1.0186),
    "distortion_supp_intermediate": (0.9489, 1.1332), "distortion_supp_large": (0.9857, 0.8554),
    "fermi_main_Qplus1": (0.89, 0.1558), "fermi_main_Qminus1": (0.91, 0.1773),
    "fermi_supp_Qplus1": (0.9015, 0.144), "fermi_supp_Qminus1": (0.926, 0.1567),
}


def evaluate(data: pd.DataFrame, distortion_manifest: pd.DataFrame, fermi_manifest: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows, predictions = [], []
    for regime in ("small", "intermediate", "large"):
        manifest = distortion_manifest[distortion_manifest["branch"].eq(regime)]
        frame = subset_from_manifest(data, manifest)
        for variant, function in (("main", distortion_main), ("supp", distortion_supplementary)):
            predicted = function(frame, regime)
            name = f"distortion_{variant}_{regime}"
            row = {"model_branch": name, "evaluation_scope": "saved held-out test", **regression_metrics(frame["Distortion_E"], predicted)}
            reported = REPORTED[name]
            row.update({"reported_R2": reported[0], "reported_RMSE": reported[1]})
            rows.append(row)
            predictions.extend({"target": "Distortion_E", "model_variant": variant, "branch": regime, "ID": int(i), "reference": float(y), "prediction": float(p), "absolute_error": abs(float(p-y))} for i, y, p in zip(frame["ID"], frame["Distortion_E"], predicted))
    for charge, tag in ((1, "Qplus1"), (-1, "Qminus1")):
        branch = f"Q_{charge:+d}"
        manifest = fermi_manifest[fermi_manifest["branch"].eq(branch)]
        frame = subset_from_manifest(data, manifest)
        for variant, function in (("main", fermi_main), ("supp", fermi_supplementary)):
            predicted = function(frame, charge)
            name = f"fermi_{variant}_{tag}"
            row = {"model_branch": name, "evaluation_scope": "saved held-out test", **regression_metrics(frame["Fermi_E"], predicted)}
            reported = REPORTED[name]
            row.update({"reported_R2": reported[0], "reported_RMSE": reported[1]})
            rows.append(row)
            predictions.extend({"target": "Fermi_E", "model_variant": variant, "branch": branch, "ID": int(i), "reference": float(y), "prediction": float(p), "absolute_error": abs(float(p-y))} for i, y, p in zip(frame["ID"], frame["Fermi_E"], predicted))
    return pd.DataFrame(rows), pd.DataFrame(predictions)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=REPOSITORY / "configs/manuscript.yaml")
    parser.add_argument("--targets", type=Path)
    parser.add_argument("--ph-features", type=Path)
    args = parser.parse_args()
    config = yaml.safe_load(args.config.read_text())
    resolve = lambda value: (REPOSITORY / value).resolve()
    targets = args.targets or resolve(config["targets"])
    features = args.ph_features or resolve(config["ph_features"])
    data = load_sources(targets, features, config.get("ph_sheet", "ph_stats_36_life_death"))
    dm = load_manifest(resolve(config["distortion_manifest"])); fm = load_manifest(resolve(config["fermi_manifest"]))
    metrics, predictions = evaluate(data, dm, fm)
    output = resolve(config["output_directory"]); (output / "metrics").mkdir(parents=True, exist_ok=True)
    metrics.to_csv(output / "metrics/heldout_metrics.csv", index=False)
    predictions.to_csv(output / "metrics/heldout_predictions.csv", index=False)
    print(metrics.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

