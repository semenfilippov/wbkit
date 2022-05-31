import pytest
from wbkit.basic import Index
from wbkit.cglimits import CGLimits
from wbkit.interpolables import Interpolable


@pytest.fixture
def fwd_dict() -> dict:
    return {
        13608: 34.45,
        14515: 33.22,
        15190: 30.14,
        19958: 22.82,
    }


@pytest.fixture
def aft_dict() -> dict:
    return {
        13608: 57.31,
        15422: 58.28,
        16329: 63.19,
        19958: 66.12,
    }


@pytest.fixture
def fwd_line(fwd_dict) -> Interpolable:
    return Interpolable([(x, y) for x, y in fwd_dict.items()])


@pytest.fixture
def aft_line(aft_dict) -> Interpolable:
    return Interpolable([(x, y) for x, y in aft_dict.items()])


@pytest.fixture
def cglimits(fwd_line, aft_line) -> CGLimits:
    return CGLimits(fwd_line, aft_line)


@pytest.fixture(params=["short_min", "short_max"])
def invalid_fwd_line(request, fwd_dict) -> Interpolable:
    if request.param == "short_min":
        _, *rest_t = fwd_dict.items()
        rest = dict(rest_t)
        return Interpolable([(x, y) for x, y in rest.items()])
    elif request.param == "short_max":
        *rest_t, _ = fwd_dict.items()
        rest = dict(rest_t)
        return Interpolable([(x, y) for x, y in rest.items()])
    else:
        raise ValueError("invalid_fwd_line internal fault")


@pytest.fixture(params=["short_min", "short_max"])
def invalid_aft_line(request, aft_dict) -> Interpolable:
    if request.param == "short_min":
        _, *rest_t = aft_dict.items()
        rest = dict(rest_t)
        return Interpolable([(x, y) for x, y in rest.items()])
    elif request.param == "short_max":
        *rest_t, _ = aft_dict.items()
        rest = dict(rest_t)
        return Interpolable([(x, y) for x, y in rest.items()])
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


def test_diff_fwd(invalid_fwd_line, aft_line):
    with pytest.raises(
        ValueError,
        match="fwd_line and aft_line min and max weights should be equal",
    ):
        CGLimits(invalid_fwd_line, aft_line)


def test_diff_aft(fwd_line, invalid_aft_line):
    with pytest.raises(
        ValueError,
        match="fwd_line and aft_line min and max weights should be equal",
    ):
        CGLimits(fwd_line, invalid_aft_line)


def test_wrong_order(fwd_line, aft_line):
    with pytest.raises(ValueError, match="make sure order of lines is fwd, aft"):
        CGLimits(aft_line, fwd_line)


def test_good_idx(cglimits, good_idx):
    assert good_idx in cglimits


def test_bad_fwd_idx(cglimits, bad_fwd_idx):
    assert bad_fwd_idx not in cglimits


def test_bad_aft_idx(cglimits, bad_aft_idx):
    assert bad_aft_idx not in cglimits
