import pytest
from crjwb.basic import calc_macrc  # noqa

ZFW = 17843
LIZFW = 29.84
MACZFW = 13.52


def test_calc_macrc():
    assert calc_macrc(LIZFW, ZFW) == pytest.approx(MACZFW, 1e-3)
