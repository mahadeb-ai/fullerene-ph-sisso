#!/usr/bin/env python3
"""Generate held-out parity panels from evaluator output."""
import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("--predictions",type=Path,default=Path("results/metrics/heldout_predictions.csv")); p.add_argument("--output",type=Path,default=Path("results/figures/heldout_prediction_panels.svg")); a=p.parse_args(); df=pd.read_csv(a.predictions); fig,axes=plt.subplots(1,2,figsize=(8,4))
    for ax,target in zip(axes,["Distortion_E","Fermi_E"]):
        part=df[(df.target==target)&(df.model_variant=="main")]; ax.scatter(part.reference,part.prediction,s=8,alpha=.55); lo=min(part.reference.min(),part.prediction.min()); hi=max(part.reference.max(),part.prediction.max()); ax.plot([lo,hi],[lo,hi],"k--",lw=1); ax.set(title=target,xlabel="Reference (eV)",ylabel="Predicted (eV)")
    fig.tight_layout(); a.output.parent.mkdir(parents=True,exist_ok=True); fig.savefig(a.output); return 0
if __name__=="__main__": raise SystemExit(main())

