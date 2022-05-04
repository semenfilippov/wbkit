import pytest
from crjwb.stab import calc_stab


def test_exceeds_fwd_limit():
    with pytest.raises(ValueError):
        calc_stab(8)


def test_exceeds_aft_limit():
    with pytest.raises(ValueError):
        calc_stab(36)


def test_calc_stab_fwd_limit():
    assert round(calc_stab(8.8), 2) == 8.15


def test_calc_stab_aft_limit():
    assert round(calc_stab(35), 2) == 4
