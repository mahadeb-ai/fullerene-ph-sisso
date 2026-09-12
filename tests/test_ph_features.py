from pathlib import Path
import numpy as np
from ph_sisso.ph.complexes import read_xyz
from ph_sisso.ph.compute_features import compute_features

FIXTURE = Path(__file__).parent / "fixtures/tetrahedron.xyz"

def test_xyz_and_feature_schema():
    points = read_xyz(FIXTURE)
    assert points.shape == (4, 3)
    assert np.isfinite(points).all()
    betti, stats = compute_features(points, max_edge_length=2.0)
    assert len(betti) == 15
    assert len(stats) == 72
    assert set(betti) == {f"betti{d}_t{t}" for d in range(3) for t in range(1, 6)}
    assert all(np.isfinite(list(stats.values())))
    assert stats["life_b0_N"] == 3.0

