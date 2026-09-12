#!/usr/bin/env python3
"""Render the representative-example CSV as a compact booktabs LaTeX table."""

from pathlib import Path
import argparse
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def render(frame: pd.DataFrame) -> str:
    lines = [r"% Requires \usepackage{booktabs}", r"\begin{table}[t]", r"\centering", r"\caption{Representative held-out fullerene predictions (eV).}", r"\begin{tabular}{lrrrrrr}", r"\toprule", "Target & ID & \\ \\ Reference & Main & Supplementary " + r"\\", r"\midrule"]
    for row in frame.itertuples(index=False):
        label = "$U_d$" if row.target == "Distortion_E" else "$E_F$"
        lines.append(f"{label} & {row.ID} & {row.Atoms} & {row.Charge:+d} & {row.reference:.3f} & {row.main_prediction:.3f} & {row.supplementary_prediction:.3f} \\\\")
    lines += ["\\bottomrule", "\\end{tabular}", "\\end{table}", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--input", type=Path, default=ROOT / "results/tables/representative_examples.csv"); parser.add_argument("--output", type=Path, default=ROOT / "results/tables/representative_examples.tex"); args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(render(pd.read_csv(args.input)), encoding="utf-8"); print(args.output); return 0


if __name__ == "__main__": raise SystemExit(main())

