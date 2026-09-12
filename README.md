# Revealing Fundamental Topology-Property Relations in Fullerene Systems

Publication software for the manuscript by Mahadeb Mandal, Benquan Wang, and
Kelin Xia. The project converts fullerene atomic point clouds into persistent-
homology (PH) descriptors, evaluates compact PH-SISSO equations on immutable
held-out partitions, reproduces representative examples and scientific panels,
and preserves the more complex Supplementary equations.

## Workflow

```text
external CSIRO structures/properties -> GUDHI Vietoris–Rips PH
-> lifetime/death descriptors -> target-specific saved splits
-> fixed main/Supplementary equations -> metrics, tables, and figures
```

Fixed-equation evaluation is inexpensive and independent of TorchSISSO.
Equation discovery is an optional, substantially more expensive workflow.

## Repository map

- `src/ph_sisso/ph/`: XYZ, Rips-complex, and PH-feature computation
- `src/ph_sisso/`: descriptor definitions, equations, splits, I/O, metrics
- `src/ph_sisso/models/`: optional selected TorchSISSO discovery interfaces
- `configs/`: scientific parameters and explicit feature mapping
- `data/splits/`: committed compact target-specific manifests
- `scripts/`: evaluation, table, figure, and robustness entry points
- `tests/`: synthetic unit tests independent of private data
- `docs/`: methods, provenance, validation, and figure mapping
- `results/`: compact reproduced metrics/tables and final traceable figures

## Data availability

Raw CSIRO fullerene data are not redistributed because the source URL/DOI and
redistribution license have not yet been verified. Follow `data/README.md`, then
run `python scripts/download_data.py`. The property table has 7,461 rows and the
canonical PH workbook has two feature sheets. Checksums prevent silent source
substitution.

## Installation

Python 3.10 and the exact locally tested core versions are recorded in
`pyproject.toml`, `requirements.txt`, and `environment.yml`:

```bash
conda env create -f environment.yml
conda activate fullerene-ph-sisso
python -m pip install -e .
```

PyArrow was not present during repository construction, so its compatible range
is specified rather than falsely labelled locally tested. It is needed only for
Parquet I/O. The audited environment contains TorchSISSO 0.1.8 from the
PaulsonLab/TorchSISSO project and PyTorch 2.10.0+cu128. Package metadata does not
identify the installed Git commit; exact discovery provenance remains an author-
review item.

## Quick start: fixed held-out evaluation

```bash
python scripts/evaluate_holdout.py --config configs/manuscript.yaml
python scripts/select_examples.py --config configs/manuscript.yaml
python scripts/reproduce_tables.py
python scripts/figures/plot_prediction_panels.py
pytest -q
```

The default config expects `data/raw/Fullerene_dataset.csv` and
`data/processed/ph_features.parquet`. Legacy workbook input is supported by
passing `--ph-features path/to/workbook.xlsx`; this reads the canonical
`ph_stats_36_life_death` sheet.

## PH computation and conventions

```bash
python scripts/compute_ph_features.py --config configs/ph.yaml
```

The calculation uses Cartesian coordinates in Å, GUDHI Rips edge filtration to
8 Å, simplices through dimension 3, coefficients in the prime field of order 11
(GUDHI canonical-script default), H0/H1/H2, five Betti
sampling points, finite-interval lifetime/death statistics, and orders
{-2,-1,1,2,3}. Exact definitions and the distinct optional ball-radius plotting
convention are documented in `docs/methods.md`.

## Equations, partitions, and expected metrics

`src/ph_sisso/equations.py` contains the rounded main and Supplementary equations
and never fits coefficients. Distortion uses separate small/intermediate/large
80/20 seed-42 partitions; Fermi uses charge-specific within-Cn target-quantile
partitions. There is intentionally no universal split and no Q=0 compact Fermi
equation. Expected held-out results are in `results/metrics/heldout_metrics.csv`.

The Supplementary Q=+1 equation uses the canonical product of squared moments,
not the superseded squared-difference form. Two quoted Supplementary distortion
RMSE values do not reproduce on the saved held-out partitions; no equation or
split was modified to force agreement. See `docs/validation.md`.

## Tables, discovery, figures, and robustness

`select_examples.py` verifies the twelve existing representative IDs against
the manifests; `reproduce_tables.py` writes CSV-backed LaTeX. Figure commands are
listed in `docs/figure_manifest.md`. Optional TorchSISSO discovery modules accept
configuration/data arguments and defer importing TorchSISSO. Manuscript-relevant
robustness entry points are in `scripts/robustness/` and do not contain local
absolute paths.

# fullerene-ph-sisso
