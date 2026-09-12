"""Selected charge-specific Fermi TorchSISSO discovery interface."""

from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
import yaml

FEATURES = ["life_b0_N", "life_b1_N", "life_b2_N", "life_b2_M_q2", "life_b2_ell_max", "death_b2_H_r2", "death_b2_H_r-2", "death_b1_M_q2", "death_b1_M_q-2", "death_b2_M_q-2"]


def fit_torchsisso(train: pd.DataFrame, target: str, n_expansion: int, n_terms: int, k: int):
    from TorchSisso import SissoModel
    table = pd.concat([train[target].rename("target"), train[FEATURES]], axis=1)
    return SissoModel(data=table, operators=["+", "-", "*", "/", "exp", "^-1", "^2"], n_expansion=n_expansion, n_term=n_terms, k=k, use_gpu=False).fit()


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--config", type=Path, required=True); parser.add_argument("--data", type=Path, required=True); args = parser.parse_args(); config = yaml.safe_load(args.config.read_text()); data = pd.read_parquet(args.data)
    print(f"Loaded {len(data)} rows; charges={config['charges']}. Apply the committed charge-specific training manifest before fitting."); return 0


if __name__ == "__main__": raise SystemExit(main())

