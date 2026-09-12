#!/usr/bin/env python3
"""Validate manually obtained external data (no verified download URL is known)."""

from __future__ import annotations
import argparse, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {"Fullerene_dataset.csv": "35cba1c4bd92463145e6781bf19e80803dbdf2806daf5a23e2c8781b27a5c1e4", "CSIRO_Data/Fullerene_data.zip": "5e21e7b32cad7921a7300f20d414dc2f110bd6711ad57250c351adf11b0ccad5"}


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1048576), b""): result.update(block)
    return result.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--data-root", type=Path, default=ROOT / "data/raw"); args = parser.parse_args(); failures = 0
    for relative, expected in EXPECTED.items():
        path = args.data_root / relative
        if not path.exists(): print(f"MISSING: {path}"); failures += 1; continue
        actual = digest(path); status = "OK" if actual == expected else "CHECKSUM MISMATCH"; print(f"{status}: {relative} sha256={actual}"); failures += actual != expected
    xyz = list((args.data_root / "CSIRO_Data").glob("*.xyz")); print(f"XYZ structures found: {len(xyz)} (expected 7461)"); failures += len(xyz) != 7461
    if failures: print("Obtain authorized CSIRO data, place it as documented in data/README.md, and retry.")
    return int(bool(failures))


if __name__ == "__main__": raise SystemExit(main())

