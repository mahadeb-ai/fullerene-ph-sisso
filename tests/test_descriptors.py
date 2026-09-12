import numpy as np
import pytest
from ph_sisso.descriptors import death_scale_entropy, ell_max, generalized_persistence_entropy, interval_values, n_k, persistence_moment

INTERVALS = np.array([[0.0, 1.0], [0.5, 2.5], [1.0, np.inf], [2.0, 2.0]])

def test_count_lifetime_and_moments():
    np.testing.assert_allclose(interval_values(INTERVALS), [1.0, 2.0])
    assert n_k(INTERVALS) == 2.0
    assert ell_max(INTERVALS) == 2.0
    assert persistence_moment(INTERVALS, 2) == 2.5
    assert persistence_moment(INTERVALS, -1) == 0.75

def test_entropy_matches_original_definition():
    values=np.array([1.0,2.0]); weights=values**2; p=weights/(weights.sum()+1e-12)
    assert generalized_persistence_entropy(INTERVALS,2) == pytest.approx(-np.sum(p*np.log(p+1e-12)))
    assert death_scale_entropy(INTERVALS,-2) == generalized_persistence_entropy(INTERVALS,-2,scale="death")

def test_zero_and_infinite_are_removed_before_negative_order():
    assert persistence_moment([[0,0],[0,np.inf]],-2) == 0.0

