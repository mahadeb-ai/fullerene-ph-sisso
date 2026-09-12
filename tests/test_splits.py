from pathlib import Path
import pandas as pd
from ph_sisso.splits import deterministic_random_split, load_manifest

ROOT=Path(__file__).resolve().parents[1]
def test_deterministic_seed():
    assert deterministic_random_split(list(range(20)),seed=42)==deterministic_random_split(list(range(20)),seed=42)
    assert deterministic_random_split(list(range(20)),seed=42)!=deterministic_random_split(list(range(20)),seed=43)

def test_canonical_manifest_counts():
    d=load_manifest(ROOT/"data/splits/distortion_main/manifest.csv"); f=load_manifest(ROOT/"data/splits/fermi_main/manifest.csv")
    assert d[d.split=="test"].groupby("branch").size().to_dict()=={"small":21,"intermediate":732,"large":740}
    assert f[f.split=="test"].groupby("branch").size().to_dict()=={"Q_-1":512,"Q_+1":511}
    assert len(d)==7461 and len(f)==4973

