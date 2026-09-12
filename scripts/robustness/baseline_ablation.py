#!/usr/bin/env python3
"""Compare fixed PH equations with mean-only held-out baselines."""
import argparse
from pathlib import Path
import pandas as pd
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("predictions",type=Path);p.add_argument("--output",type=Path,required=True);a=p.parse_args();d=pd.read_csv(a.predictions);rows=[]
 for keys,g in d.groupby(["target","model_variant","branch"]):rows.append({"target":keys[0],"model_variant":keys[1],"branch":keys[2],"mae":(g.prediction-g.reference).abs().mean(),"mean_baseline_mae":(g.reference-g.reference.mean()).abs().mean()})
 a.output.parent.mkdir(parents=True,exist_ok=True);pd.DataFrame(rows).to_csv(a.output,index=False);return 0
if __name__=="__main__":raise SystemExit(main())

