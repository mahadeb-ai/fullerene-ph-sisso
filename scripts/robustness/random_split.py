#!/usr/bin/env python3
"""Evaluate fixed equations across deterministic random splits (S12-style analysis)."""
import argparse,sys
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/"src"))
from ph_sisso.splits import deterministic_random_split
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("data",type=Path);p.add_argument("--seeds",type=int,nargs="+",default=[0,1,2,3,42]);p.add_argument("--output",type=Path,required=True);a=p.parse_args();df=pd.read_parquet(a.data);rows=[]
 for seed in a.seeds:
  assignment=deterministic_random_split(df.ID.astype(int).tolist(),seed=seed);rows.extend({"ID":i,"seed":seed,"split":s} for i,s in assignment.items())
 a.output.parent.mkdir(parents=True,exist_ok=True);pd.DataFrame(rows).to_csv(a.output,index=False);return 0
if __name__=="__main__":raise SystemExit(main())

