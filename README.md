# Revealing Fundamental Topology-Property Relations in Fullerene Systems

This repository contains the Python code used in the manuscript by Mahadeb Mandal, Benquan Wang, and Kelin Xia. It converts fullerene atomic point clouds into persistent-homology (PH) descriptors, evaluates the compact PH-SISSO equations on fixed held-out partitions, reproduces representative results and scientific figures, and includes the higher-complexity Supplementary equations.

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

The fullerene structures and SCC–DFTB-derived properties used in this study are publicly available through the CSIRO Fullerene Data Set:

https://data.csiro.au/collection/csiro:59022

## Installation

Python 3.10 and the exact locally tested core versions are recorded in
`pyproject.toml`, `requirements.txt`, and `environment.yml`:

```bash
conda env create -f environment.yml
conda activate fullerene-ph-sisso
python -m pip install -e .
```

PyArrow was not installed in the environment used to construct and validate this repository; therefore, a compatible version range is specified rather than a locally tested version. PyArrow is required only for Parquet I/O. The validated environment used TorchSISSO 0.1.8 from the PaulsonLab/TorchSISSO project and PyTorch 2.10.0+cu128.

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

The calculation uses Cartesian coordinates in Å and constructs GUDHI Vietoris–Rips complexes with a maximum edge length of 8 Å. Simplices are generated through dimension 3, with homology computed in dimensions H0, H1, and H2 using coefficients in the prime field of order 11. The descriptor set includes five Betti sampling points, finite-interval lifetime and death-scale statistics, and generalized orders {-2, -1, 1, 2, 3}. Exact definitions and the optional ball-radius convention used for plotting are documented in `docs/methods.md`.

## Equations, partitions, and expected metrics

`src/ph_sisso/equations.py` contains the fixed main-text and Supplementary equations and evaluates them without refitting their coefficients. Distortion-energy models use separate 80/20 partitions for the small-, intermediate-, and large-cage regimes with random seed 42, whereas the Fermi-energy models use charge-specific, within-\(C_n\) target-quantile partitions. The corresponding held-out metrics are reported in `results/metrics/heldout_metrics.csv`.

## Tables, discovery, figures, and robustness

`select_examples.py` verifies the twelve representative IDs against the saved split manifests, while `reproduce_tables.py` generates the corresponding CSV and LaTeX tables. Figure-generation commands are documented in `docs/figure_manifest.md`. Optional TorchSISSO modules provide the equation-discovery workflows used in the study. Manuscript-related robustness analyses are available in `scripts/robustness/` and use portable, configurable paths.
