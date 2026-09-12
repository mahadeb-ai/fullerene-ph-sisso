#!/usr/bin/env python3
"""Compute and plot an H2 barcode, optionally on the ball-radius scale."""
import argparse,sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/"src"))
from ph_sisso.ph.complexes import build_rips_complex,read_xyz

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("xyz",type=Path); p.add_argument("--output",type=Path,default=ROOT/"results/figures/h2_barcode.svg"); p.add_argument("--ball-radius",action="store_true"); a=p.parse_args(); tree=build_rips_complex(read_xyz(a.xyz)); intervals=np.asarray(tree.persistence_intervals_in_dimension(2),float).reshape(-1,2); scale=0.5 if a.ball_radius else 1.0; intervals=intervals*scale
    fig,ax=plt.subplots(figsize=(5,3)); finite=intervals[np.isfinite(intervals[:,1])]
    for y,(birth,death) in enumerate(finite): ax.hlines(y,birth,death,lw=2)
    ax.set_xlabel("Ball radius, $r=\\epsilon/2$ (Å)" if a.ball_radius else "Rips edge filtration, $\\epsilon$ (Å)"); ax.set_ylabel("$H_2$ interval"); fig.tight_layout(); a.output.parent.mkdir(parents=True,exist_ok=True); fig.savefig(a.output); return 0
if __name__=="__main__": raise SystemExit(main())

