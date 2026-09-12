from pathlib import Path
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]

def test_representative_ids_and_selected_predictions():
    frame = pd.read_csv(ROOT / "results/tables/representative_examples.csv")
    distortion = frame[frame.target == "Distortion_E"]
    fermi = frame[frame.target == "Fermi_E"]
    assert distortion.ID.tolist() == [32, 4985, 360, 5806, 2283, 7033]
    assert fermi.ID.tolist() == [1665, 955, 401, 2916, 3700, 4169]
    assert distortion.iloc[0].main_prediction == pytest.approx(32.297149, abs=1e-6)
    assert distortion.iloc[-1].supplementary_prediction == pytest.approx(46.206873, abs=1e-6)
    assert fermi.iloc[0].supplementary_prediction == pytest.approx(-1.822791, abs=1e-6)
    assert fermi.iloc[-1].main_prediction == pytest.approx(-8.096942, abs=1e-6)

