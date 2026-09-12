import numpy as np
import pandas as pd
import pytest
from ph_sisso.equations import distortion_main, distortion_supplementary, fermi_main, fermi_supplementary

def row(atoms=30,charge=1):
    return pd.DataFrame({"Atoms":[atoms],"Charge":[charge],"life_b0_N":[10.0],"life_b1_N":[8.0],"life_b2_N":[2.0],"life_b2_M_q2":[4.0],"life_b2_ell_max":[3.0],"life_b0_H_r3":[2.0],"life_b0_H_r-2":[5.0],"death_b2_H_r2":[1.5],"death_b2_H_r-2":[2.5],"death_b1_M_q2":[2.0],"death_b1_M_q-2":[.5],"death_b2_M_q-2":[.25]})

def test_fixed_distortion_equations():
    d=row(); assert distortion_main(d,"small")[0]==pytest.approx(.09*10/4+3.98*np.exp(1)+23.087)
    assert distortion_supplementary(d,"small")[0]==pytest.approx(.075*10/4-4.65*4+4.65+2.36+30.19)

def test_product_form_and_qzero_unsupported():
    d=row(); expected=2699.60*(2/10)*1.5*(.5**2)*(.25**2)-10.21
    assert fermi_supplementary(d,1)[0]==pytest.approx(expected)
    assert fermi_main(d,1)[0]==pytest.approx(.9*1.5-11.26)
    with pytest.raises(ValueError): fermi_main(d,0)
    with pytest.raises(ValueError): fermi_supplementary(d,0)

def test_qminus_supplementary():
    d=row(charge=-1); expected=16.48*(10/8)*(-1)*(1/(2*.5))+29.87
    assert fermi_supplementary(d,-1)[0]==pytest.approx(expected)

