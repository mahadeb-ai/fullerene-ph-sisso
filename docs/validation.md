# Scientific validation and known provenance warnings

Fixed equations were evaluated without refitting on target-specific seed-42
manifests extracted from the authoritative saved research partitions. The main
distortion branches contain 21, 732, and 740 test structures. Fermi branches
contain 512 Q=-1 and 511 Q=+1 structures.

The canonical audit tolerance is absolute R2 difference <= 0.02 and RMSE
difference <= max(0.02 eV, 5%). All main-equation metrics, both Supplementary
Fermi metrics, and all reported R2 values pass. Supplementary distortion RMSE
has unresolved provenance differences: the quoted small-regime 1.0186 eV is
1.09279 eV on the saved test, and the quoted large-regime 0.8554 eV is 0.99034
eV on the saved test. These equations and splits were not adjusted. The quoted
intermediate and large Supplementary values are closer to evaluation over all
rows in their regimes (approximately 1.13315 and 0.85565 eV) than to their saved
held-out tests. See `results/metrics/validation_report.md` for the complete table.

