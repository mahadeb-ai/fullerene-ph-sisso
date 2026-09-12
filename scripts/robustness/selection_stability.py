#!/usr/bin/env python3
"""Summarize descriptor occurrence across saved SISSO equation text/CSV files."""
import argparse,re
from pathlib import Path
from collections import Counter
import pandas as pd
def main()->int:
 p=argparse.ArgumentParser();p.add_argument("inputs",type=Path,nargs="+");p.add_argument("--output",type=Path,required=True);a=p.parse_args();counter=Counter()
 for path in a.inputs:
  for descriptor in re.findall(r"(?:life|death)_b[012]_[A-Za-z0-9_-]+",path.read_text(errors="ignore")):counter[descriptor]+=1
 a.output.parent.mkdir(parents=True,exist_ok=True);pd.DataFrame(counter.most_common(),columns=["descriptor","count"]).to_csv(a.output,index=False);return 0
if __name__=="__main__":raise SystemExit(main())

