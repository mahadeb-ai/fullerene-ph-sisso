#!/usr/bin/env python3
"""Summarize PH descriptor distributions by charge state."""
import argparse
from pathlib import Path
import pandas as pd
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("data",type=Path);p.add_argument("--output",type=Path,required=True);a=p.parse_args();d=pd.read_parquet(a.data);features=[c for c in d if c.startswith(("life_","death_"))];out=d.groupby("Charge")[features].agg(["mean","std","min","max"]);a.output.parent.mkdir(parents=True,exist_ok=True);out.to_csv(a.output);return 0
if __name__=="__main__":raise SystemExit(main())

