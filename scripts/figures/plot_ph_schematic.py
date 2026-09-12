#!/usr/bin/env python3
"""Draw a self-contained persistence-barcode descriptor schematic."""
import argparse
from pathlib import Path
import matplotlib.pyplot as plt


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--output",type=Path,default=Path("results/figures/ph_schematic.svg")); args=parser.parse_args()
    bars=[(0.0,1.0),(0.2,1.8),(0.6,2.2),(1.1,2.7)]; fig,ax=plt.subplots(figsize=(5,3))
    for y,(birth,death) in enumerate(bars): ax.hlines(y,birth,death,lw=3); ax.scatter([birth,death],[y,y],s=18)
    ax.set(xlabel="Rips edge filtration, $\\epsilon$ (Å)",ylabel="feature index",title="Persistence intervals"); fig.tight_layout(); args.output.parent.mkdir(parents=True,exist_ok=True); fig.savefig(args.output); return 0
if __name__=="__main__": raise SystemExit(main())

