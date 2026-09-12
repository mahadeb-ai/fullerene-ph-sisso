# Figure manifest

| Figure/panel | Source script | Input data | Command | Expected output | Notes |
|---|---|---|---|---|---|
| PH barcode schematic | `scripts/figures/plot_ph_schematic.py` | none | `python scripts/figures/plot_ph_schematic.py` | `results/figures/ph_schematic.svg` | Edge-filtration scale. |
| H2 barcode example | `scripts/figures/plot_h2_barcodes.py` | one authorized XYZ | `python scripts/figures/plot_h2_barcodes.py data/raw/CSIRO_Data/FILE.xyz` | `results/figures/h2_barcode.svg` | Add `--ball-radius` only for an explicitly radius-labelled panel. |
| Main held-out parity panels | `scripts/figures/plot_prediction_panels.py` | `results/metrics/heldout_predictions.csv` | `python scripts/figures/plot_prediction_panels.py` | `results/figures/heldout_prediction_panels.svg` | Generated after evaluation. |
| Conceptual topology/property artwork | external manuscript artwork | author source | not automated | manuscript asset | Presentation-only art is intentionally not approximated. |

