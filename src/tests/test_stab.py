import pytest
from crjwb.stab import Stab


@pytest.fixture(scope="module")
def stab():
    yield Stab({8.8: 8.15, 35: 4})


def test_one_point():
    with pytest.raises(ValueError):
        Stab({1.1: 2.1})


def test_exceeds_fwd_limit(stab: Stab):
    with pytest.raises(ValueError):
        stab.calc(8)


def test_exceeds_aft_limit(stab: Stab):
    with pytest.raises(ValueError):
        stab.calc(36)


def test_calc(stab: Stab):
    assert round(stab.calc(12.58), 2) == 7.55


def test_calc_stab_fwd_limit(stab: Stab):
    assert round(stab.calc(8.8), 2) == 8.15


def test_calc_stab_aft_limit(stab: Stab):
    assert round(stab.calc(35), 2) == 4
