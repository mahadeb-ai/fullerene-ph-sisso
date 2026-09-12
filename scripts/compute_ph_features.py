#!/usr/bin/env python3
"""CLI for the canonical PH feature generator."""

import argparse, sys
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from ph_sisso.ph.compute_features import compute_dataset


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--config", type=Path, default=ROOT / "configs/ph.yaml"); parser.add_argument("--input", type=Path); parser.add_argument("--xyz-dir", type=Path); parser.add_argument("--output", type=Path); args = parser.parse_args()
    config = yaml.safe_load(args.config.read_text()); resolve = lambda value: (ROOT / value).resolve()
    compute_dataset(args.input or resolve(config["input_table"]), args.xyz_dir or resolve(config["xyz_directory"]), args.output or resolve(config["output"]), max_edge_length=float(config["max_edge_length_angstrom"]), max_dimension=int(config["max_simplex_dimension"]), homology_coeff_field=int(config["homology_coeff_field"]), betti_filtrations=tuple(config["betti_filtrations"]))
    return 0


if __name__ == "__main__": raise SystemExit(main())

