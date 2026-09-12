"""Configurable TorchSISSO discovery for the three distortion size regimes.

This expensive optional workflow is intentionally separate from fixed-equation
evaluation. It exposes the manuscript feature pool and canonical manifests but
does not execute on import.
"""

from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
import yaml

FEATURES = ["life_b0_N", "life_b1_N", "life_b2_N", "life_b2_M_q2", "life_b2_ell_max", "life_b0_H_r3", "life_b0_H_r-2", "Charge"]


def fit_torchsisso(train: pd.DataFrame, target: str, n_expansion: int, n_terms: int, k: int):
    """Fit one TorchSISSO configuration; importing TorchSISSO is deferred."""
    from TorchSisso import SissoModel
    table = pd.concat([train[target].rename("target"), train[FEATURES]], axis=1)
    model = SissoModel(data=table, operators=["+", "-", "*", "/", "exp", "^-1", "^2"], n_expansion=n_expansion, n_term=n_terms, k=k, use_gpu=False)
    return model.fit()


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--config", type=Path, required=True); parser.add_argument("--data", type=Path, required=True); args = parser.parse_args(); config = yaml.safe_load(args.config.read_text()); data = pd.read_parquet(args.data)
    print(f"Loaded {len(data)} rows. Use the committed distortion manifest to select training rows before calling fit_torchsisso().")
    print(f"Configured discovery grid: {config.get('discovery')}"); return 0


if __name__ == "__main__": raise SystemExit(main())

