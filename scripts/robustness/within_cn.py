#!/usr/bin/env python3
"""Within-Cn correlations after subtracting each Cn target mean."""
import argparse
from pathlib import Path
import pandas as pd
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("data",type=Path);p.add_argument("--target",default="Distortion_E");p.add_argument("--features",nargs="+",required=True);p.add_argument("--output",type=Path,required=True);a=p.parse_args();d=pd.read_parquet(a.data);d["residual"]=d[a.target]-d.groupby("Atoms")[a.target].transform("mean");rows=[{"feature":f,"pearson":d[[f,"residual"]].corr().iloc[0,1]} for f in a.features];a.output.parent.mkdir(parents=True,exist_ok=True);pd.DataFrame(rows).to_csv(a.output,index=False);return 0
if __name__=="__main__":raise SystemExit(main())

