import numpy as np
import pytest
from ph_sisso.metrics import regression_metrics

def test_metrics():
    result=regression_metrics([1,2,3],[1,2,4])
    assert result["N_test"]==3
    assert result["RMSE"]==pytest.approx(np.sqrt(1/3))
    assert result["MAE"]==pytest.approx(1/3)
    assert result["mean_error"]==pytest.approx(1/3)
    assert result["median_absolute_error"]==0
    assert result["maximum_absolute_error"]==1
    assert result["R2"]==pytest.approx(.5)

