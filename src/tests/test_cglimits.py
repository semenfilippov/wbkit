import pytest
from wbkit.basic import Index
from wbkit.cglimits import CGLimits
from wbkit.interpolables import Interpolable


@pytest.fixture(params=["short_min", "short_max"])
def invalid_fwd_line(request, fwd_zfw_dict) -> Interpolable:
    if request.param == "short_min":
        _, *rest_t = fwd_zfw_dict.items()
        rest = dict(rest_t)
        return Interpolable([*rest.items()])
    elif request.param == "short_max":
        *rest_t, _ = fwd_zfw_dict.items()
        rest = dict(rest_t)
        return Interpolable([*rest.items()])
    else:
        raise ValueError("invalid_fwd_line internal fault")


@pytest.fixture(params=["short_min", "short_max"])
def invalid_aft_line(request, aft_zfw_dict) -> Interpolable:
    if request.param == "short_min":
        _, *rest_t = aft_zfw_dict.items()
        rest = dict(rest_t)
        return Interpolable([*rest.items()])
    elif request.param == "short_max":
        *rest_t, _ = aft_zfw_dict.items()
        rest = dict(rest_t)
        return Interpolable([*rest.items()])
    else:
        raise ValueError("invalid_aft_line internal fault")


@pytest.fixture
def good_idx(rck) -> Index:
    return Index(29.84, 17841, rck)


@pytest.fixture
def bad_fwd_idx(rck) -> Index:
    return Index(33, 14500, rck)


@pytest.fixture
def bad_aft_idx(rck) -> Index:
    return Index(59, 15400, rck)


def test_diff_fwd(invalid_fwd_line, zfw_aft_line):
    with pytest.raises(
        ValueError,
        match="fwd_line and aft_line min and max weights should be equal",
    ):
        CGLimits(invalid_fwd_line, zfw_aft_line)


def test_diff_aft(zfw_fwd_line, invalid_aft_line):
    with pytest.raises(
        ValueError,
        match="fwd_line and aft_line min and max weights should be equal",
    ):
        CGLimits(zfw_fwd_line, invalid_aft_line)


def test_wrong_order(zfw_fwd_line, zfw_aft_line):
    with pytest.raises(ValueError, match="make sure order of lines is fwd, aft"):
        CGLimits(zfw_aft_line, zfw_fwd_line)


def test_good_idx(zfw_cglimits, good_idx):
    assert good_idx in zfw_cglimits


def test_bad_fwd_idx(zfw_cglimits, bad_fwd_idx):
    assert bad_fwd_idx not in zfw_cglimits


def test_bad_aft_idx(zfw_cglimits, bad_aft_idx):
    assert bad_aft_idx not in zfw_cglimits
