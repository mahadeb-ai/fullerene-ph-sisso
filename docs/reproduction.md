# Reproduction guide

From the repository root, install with `python -m pip install -e '.[dev]'`.
Place authorized raw data as described in `data/README.md`. To validate them:

```bash
python scripts/download_data.py
```

To regenerate PH features (computationally expensive):

```bash
python scripts/compute_ph_features.py --config configs/ph.yaml
```

To evaluate fixed equations and generate tables:

```bash
python scripts/evaluate_holdout.py --config configs/manuscript.yaml
python scripts/select_examples.py --config configs/manuscript.yaml
python scripts/reproduce_tables.py
```

Then generate the traceable prediction panel and run tests:

```bash
python scripts/figures/plot_prediction_panels.py
pytest -q
```

Discovery is optional and requires TorchSISSO. It is separate from inexpensive
fixed-equation validation; consult the three modules in `src/ph_sisso/models/`.

