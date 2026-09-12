"""Selected extended-descriptor TorchSISSO discovery definitions."""

from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd


def add_extended_descriptors(frame: pd.DataFrame) -> pd.DataFrame:
    """Add the two documented Supplementary Fermi composite inputs."""
    result = frame.copy()
    result["qplus_product_input"] = result["life_b2_N"] / result["life_b0_N"] * result["death_b2_H_r2"] * result["death_b1_M_q-2"]**2 * result["death_b2_M_q-2"]**2
    result["qminus_rho_mu_input"] = -(result["life_b0_N"] / result["life_b1_N"]) / (result["death_b1_M_q2"] * result["death_b1_M_q-2"])
    return result


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--data", type=Path, required=True); parser.add_argument("--output", type=Path, required=True); args = parser.parse_args(); data = add_extended_descriptors(pd.read_parquet(args.data)); args.output.parent.mkdir(parents=True, exist_ok=True); data.to_parquet(args.output, index=False); return 0


if __name__ == "__main__": raise SystemExit(main())

