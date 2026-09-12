# Held-out metric validation

All values use the immutable target-specific test manifests and rounded fixed
equations. No fitting or coefficient adjustment was performed.

| Model branch | N | Reported R2 | Reproduced R2 | Reported RMSE | Reproduced RMSE | Status |
|---|---:|---:|---:|---:|---:|---|
| distortion_main_small | 21 | 0.9690 | 0.967500 | 1.0120 | 1.032339 | PASS |
| distortion_main_intermediate | 732 | 0.9360 | 0.935631 | 1.2840 | 1.284083 | PASS |
| distortion_main_large | 740 | 0.9610 | 0.960480 | 1.3800 | 1.387764 | PASS |
| distortion_supp_small | 21 | 0.9522 | 0.963582 | 1.0186 | 1.092786 | **WARNING: RMSE** |
| distortion_supp_intermediate | 732 | 0.9489 | 0.951253 | 1.1332 | 1.117456 | PASS |
| distortion_supp_large | 740 | 0.9857 | 0.979874 | 0.8554 | 0.990340 | **WARNING: RMSE** |
| fermi_main_Qplus1 | 511 | 0.8900 | 0.889920 | 0.1558 | 0.152632 | PASS |
| fermi_main_Qminus1 | 512 | 0.9100 | 0.911822 | 0.1773 | 0.170907 | PASS |
| fermi_supp_Qplus1 | 511 | 0.9015 | 0.901500 | 0.1440 | 0.144381 | PASS |
| fermi_supp_Qminus1 | 512 | 0.9260 | 0.925060 | 0.1567 | 0.157557 | PASS |

Tolerance follows the canonical audit: absolute R2 difference <= 0.02 and RMSE
difference <= max(0.02 eV, 5%). The Supplementary distortion warnings are not
repaired. The quoted intermediate and large Supplementary distortion values are
closer to all-regime-row evaluations (RMSE 1.13315 and 0.85565 eV) than to saved
test evaluation; the small quoted value is also closer to its all-regime value
(1.02140 eV) than to its saved-test value.

