import pytest
from crjwb.basic import calc_index, calc_macrc  # noqa

ZFW = 17843
LIZFW = 29.84
MACZFW = 13.52


def test_calc_index():
    """
    ``calc_index`` function is not used anywhere, and its purpose \
    is unclear yet, so there is no point in testing it
    """
    pytest.skip()


def test_calc_macrc():
    assert calc_macrc(LIZFW, ZFW) == pytest.approx(MACZFW, 1e-3)
