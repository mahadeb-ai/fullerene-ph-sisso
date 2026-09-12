# Computational methods and conventions

## Persistent homology

Each optimized fullerene geometry is treated as an unweighted point cloud of
carbon-atom Cartesian coordinates in Angstrom. GUDHI constructs a
Vietoris–Rips complex using pairwise Euclidean distances. The filtration value
`epsilon` is the maximum **edge length** admitted to the complex; it is not the
radius of balls around atoms. A ball-radius visualization may use
`r = epsilon/2`, but that conversion is figure-specific and is never applied to
the canonical feature table.

The maximum Rips edge length is 8.0 Å. Simplices are constructed through
dimension 3 so that two-dimensional classes can both appear and die. Persistent
homology is calculated over the prime field with 11 elements, preserving the
GUDHI default used by the canonical feature generator, in H0, H1,
and H2. Betti numbers use the half-open convention `birth <= t < death` and are
sampled at edge-filtration values 1, 2, 3, 4, and 5 Å.

The historical H2-barcode figure script explicitly used coefficient field 2,
whereas the canonical feature generator used GUDHI default field 11. The
refactored figure script defaults to field 11 so it cannot silently disagree
with the feature table; any field-2 legacy-panel reproduction must be explicitly
labelled as figure-specific.

For an interval `(b_i,d_i)`, lifetime is `l_i=d_i-b_i`. Infinite-death
intervals are excluded from all scalar lifetime/death statistics. Non-positive
lifetimes are removed; death-scale descriptors likewise retain only strictly
positive death values. This filtering occurs before negative powers are taken.

For each homology dimension and for both `x_i=l_i` (prefix `life_`) and
`x_i=d_i` (prefix `death_`), the descriptors are:

- `N`: number of retained values;
- `ell_max`: `max_i x_i`, or zero for an empty set;
- moment `M_q = mean_i(x_i^q)` for `q in {-2,-1,1,2,3}`;
- order-weighted entropy: `w_i=x_i^r`,
  `p_i=w_i/(sum_j w_j + 1e-12)`, and
  `H_r=-sum_i p_i log(p_i+1e-12)` for
  `r in {-2,-1,1,2,3}`.

Empty descriptors return zero, matching the canonical research implementation.
The `1e-12` constants and positive-value filters are preserved; they should not
be changed without creating a new dataset version.

## Fixed equations

All public held-out evaluation uses the rounded coefficients printed in the
manuscript and performs no fitting. Distortion has three atom-count branches:
`n <= 36`, `36 < n <= 76`, and `n > 76`. Fermi models exist only for charges
Q=+1 and Q=-1. Equations are encoded in `src/ph_sisso/equations.py`; symbol-to-
column semantics are explicit in `configs/feature_mapping.json`.

The Supplementary Q=+1 Fermi equation uses the product
`(N2/N0) Hd_2_2 (Md_1_minus2)^2 (Md_2_minus2)^2`. The earlier squared
difference interpretation is not part of this repository.

