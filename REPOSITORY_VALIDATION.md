# Repository validation

Validation date: 2026-09-13.

## 1. Refactored scientific material

- The canonical `FeatTopo.py` behavior was separated into XYZ/Rips construction,
  explicit descriptor functions, dataset feature generation, and a thin CLI.
- The canonical fixed-equation evaluator was separated into portable I/O,
  equations, metrics, split handling, evaluation, representative selection, and
  table rendering.
- Selected distortion, Fermi, and extended-descriptor discovery interfaces were
  extracted into optional modules that do not execute or import TorchSISSO at
  import time.
- Six manuscript-relevant robustness analyses were reduced to configurable,
  path-independent entry points.
- Three traceable scientific figure scripts were created; presentation-only
  conceptual art was not copied.

No original research file was edited, moved, renamed, or deleted. No Git
repository was initialized.

## 2. Deliberate exclusions

SWCNT, CNR/nanoribbon, KAN, fingerprint projects, broad bandgap/EA/IP
experiments, obsolete monolithic SISSO scripts, duplicate random-state/result
trees, full train/test feature tables, worker pickles, logs, caches, checkpoints,
and bulk images were excluded. Raw CSIRO data and the derived Excel workbook were
not copied into the clean repository.

## 3. Equations implemented

`src/ph_sisso/equations.py` implements all three main and Supplementary
distortion branches, the Q=+1/Q=-1 main Fermi equations, and both Supplementary
Fermi equations. Q=0 Fermi evaluation raises an explicit unsupported error. The
Supplementary Q=+1 equation is the canonical product of squared moments; the
superseded squared-difference form is absent. All evaluation is prediction-only.

## 4. PH conventions

Coordinates are Cartesian Å values. The canonical feature workflow uses GUDHI
Vietoris–Rips edge filtration, maximum edge 8.0 Å, simplices through dimension
3, H0/H1/H2, and GUDHI's canonical-script default prime coefficient field 11.
It filters infinite deaths, retains positive lifetime/death values, and uses the
original `1e-12` stabilization. Orders are -2, -1, 1, 2, and 3; Betti sampling
points are 1–5 Å. Ball radius `r=epsilon/2` is an explicitly labelled plotting
conversion, not a feature-table convention.

## 5. Train/test protocols and counts

There is no universal split. Distortion uses per-regime random-row 80/20 splits
with seed 42; test counts are small 21, intermediate 732, large 740 (total
1,493). Fermi uses charge-specific within-Cn target-quantile isomer 80/20 splits
with seed 42; counts are Q=-1 512 and Q=+1 511 (total 1,023). Manifests contain
7,461 and 4,973 complete assignments respectively, no missing cells, and source
split-file SHA-256 values.

## 6. Representative examples

All IDs were verified against their appropriate held-out branch. Distortion:
32, 4985, 360, 5806, 2283, 7033. Fermi Q=-1: 1665, 955, 401. Fermi Q=+1:
2916, 3700, 4169. CSV and LaTeX outputs are under `results/tables/`.

## 7. Reproduced metrics

| Branch | N | R2 | RMSE (eV) |
|---|---:|---:|---:|
| distortion_main_small | 21 | 0.967500 | 1.032339 |
| distortion_main_intermediate | 732 | 0.935631 | 1.284083 |
| distortion_main_large | 740 | 0.960480 | 1.387764 |
| distortion_supp_small | 21 | 0.963582 | 1.092786 |
| distortion_supp_intermediate | 732 | 0.951253 | 1.117456 |
| distortion_supp_large | 740 | 0.979874 | 0.990340 |
| fermi_main_Qplus1 | 511 | 0.889920 | 0.152632 |
| fermi_main_Qminus1 | 512 | 0.911822 | 0.170907 |
| fermi_supp_Qplus1 | 511 | 0.901500 | 0.144381 |
| fermi_supp_Qminus1 | 512 | 0.925060 | 0.157557 |

Every numeric metric (R2, RMSE, MAE, mean error, median absolute error, maximum
absolute error, and N) agrees exactly with the prior canonical evaluator output;
the maximum numeric difference was 0.0.

## 8. Manuscript-value differences

The Supplementary distortion small quoted RMSE 1.0186 eV reproduces as 1.092786
eV on its saved test; the large quoted 0.8554 eV reproduces as 0.990340 eV.
These exceed the canonical 5%/0.02 eV tolerance. Equations and partitions were
not changed. Full-regime values (small approximately 1.02140 eV; intermediate
1.13315 eV; large 0.85565 eV) explain the likely provenance, especially for the
intermediate/large quoted values. All R2 values and other reported held-out
metrics pass the audit tolerance.

## 9. TorchSISSO status

The Python 3.10 evaluation environment contains distribution `TorchSisso` 0.1.8
at a standard environment site-packages location and PyTorch 2.10.0+cu128.
Package metadata identifies the PaulsonLab/TorchSISSO GitHub project and an MIT
classifier but does not record the installed Git commit. Exact commit provenance
is unresolved. Core fixed-equation evaluation and tests do not require it.

## 10. External-data status

The current property CSV, source ZIP, derived PH workbook, and aggregate sorted
XYZ checksum are recorded in `data/`. Original CSIRO DOI/URL, full citation,
retrieval date, redistribution permission, and charge-state geometry protocol
remain unresolved. Raw/processed data are ignored and absent from the repository.

## 11. Tests and safety

`conda run -n base pytest -q` completed with **11 passed** and two non-failing
warnings about old optional numexpr/bottleneck versions in that existing test
environment. Syntax compilation passed. Full-data evaluation was separately run
under the Python 3.10 scientific environment. The recursive publication scan
found no embedded personal absolute path, credential, private key, intentional
email, log, pickle, checkpoint, source data, or cache after cleanup. See `PUBLICATION_SAFETY_REPORT.md`.

## 12. Exact validated commands

From the clean repository root, with authorized source files available:

```bash
python scripts/evaluate_holdout.py --config configs/manuscript.yaml \
  --targets PATH/Fullerene_dataset.csv \
  --ph-features PATH/topology_rips_features_fullerene_ALL.xlsx
python scripts/select_examples.py --config configs/manuscript.yaml \
  --targets PATH/Fullerene_dataset.csv \
  --ph-features PATH/topology_rips_features_fullerene_ALL.xlsx
python scripts/reproduce_tables.py
python scripts/figures/plot_prediction_panels.py
conda run -n base pytest -q
```

For the public default layout, omit path overrides after producing
`data/processed/ph_features.parquet` from authorized raw data.


