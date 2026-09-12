#!/usr/bin/env python3
"""Report sample counts under alternative distortion regime boundaries."""
import argparse
from pathlib import Path
import pandas as pd
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("data",type=Path);p.add_argument("--lower",type=int,nargs="+",default=[34,36,38]);p.add_argument("--upper",type=int,nargs="+",default=[74,76,78]);p.add_argument("--output",type=Path,required=True);a=p.parse_args();d=pd.read_parquet(a.data);rows=[]
 for lo in a.lower:
  for hi in a.upper:rows.append({"lower_boundary":lo,"upper_boundary":hi,"small":int((d.Atoms<=lo).sum()),"intermediate":int(((d.Atoms>lo)&(d.Atoms<=hi)).sum()),"large":int((d.Atoms>hi).sum())})
 a.output.parent.mkdir(parents=True,exist_ok=True);pd.DataFrame(rows).to_csv(a.output,index=False);return 0
if __name__=="__main__":raise SystemExit(main())

