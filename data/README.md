# Data setup and provenance

Source structures and properties were supplied as the **CSIRO fullerene data**.
The audited workspace does not contain a verified DOI, download URL, license, or
retrieval date. Consequently, this repository does not redistribute the data.
The authors must add the original CSIRO citation and confirm redistribution terms
before release.

Place authorized copies as follows:

```text
data/raw/
├── Fullerene_dataset.csv          # 7,461 rows; 886 columns
└── CSIRO_Data/
    ├── 0001.xyz
    ├── ...                        # 7,461 XYZ structures in total
    ├── 7461.xyz                   # IDs need not be contiguous in meaning
    └── Fullerene_data.zip         # optional; not needed if extracted
```

The current property table checksum is recorded in `checksums.sha256`. The ZIP
checksum is also recorded, but users should avoid retaining both archive and
extraction unnecessarily. The aggregate digest of the sorted `sha256sum` listing
for the 7,461 current XYZ files is
`1b375bfe2a336c6f310c7004aa06aad3c93b514f36d6899f7a136369a4550608`.

The derived canonical workbook has 7,461 rows and two sheets,
`betti_curve_15` and `ph_stats_36_life_death`. Its expected checksum is listed
under the legacy filename in `checksums.sha256`. Regenerate a portable Parquet
table with `python scripts/compute_ph_features.py`. `data/raw/` and
`data/processed/` are ignored by Git. A versioned GitHub Release or Zenodo record
is recommended for derived features after data permissions are resolved.

