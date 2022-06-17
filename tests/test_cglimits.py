import pytest
from wbkit.cglimits import CG, CGLimits
from wbkit.plfunc import PLFunction


@pytest.fixture
def fwd_zfw_dict() -> dict:
    return {
        13608: 34.45,
        14515: 33.22,
        15190: 30.14,
        19958: 22.82,
    }


@pytest.fixture
def aft_zfw_dict() -> dict:
    return {
        13608: 57.31,
        15422: 58.28,
        16329: 63.19,
        19958: 66.12,
    }


@pytest.fixture
def zfw_fwd_line(fwd_zfw_dict) -> PLFunction:
    return PLFunction([*fwd_zfw_dict.items()])


@pytest.fixture
def zfw_aft_line(aft_zfw_dict) -> PLFunction:
    return PLFunction([*aft_zfw_dict.items()])


@pytest.fixture
def zfw_cglimits(zfw_fwd_line, zfw_aft_line) -> CGLimits:
    return CGLimits(zfw_fwd_line, zfw_aft_line)


@pytest.fixture(params=["short_min", "short_max"])
def invalid_fwd_line(request, fwd_zfw_dict) -> PLFunction:
    if request.param == "short_min":
        _, *rest_t = fwd_zfw_dict.items()
        rest = dict(rest_t)
        return PLFunction([*rest.items()])
    elif request.param == "short_max":
        *rest_t, _ = fwd_zfw_dict.items()
        rest = dict(rest_t)
        return PLFunction([*rest.items()])
    else:
        raise ValueError("invalid_fwd_line internal fault")


@pytest.fixture(params=["short_min", "short_max"])
def invalid_aft_line(request, aft_zfw_dict) -> PLFunction:
    if request.param == "short_min":
        _, *rest_t = aft_zfw_dict.items()
        rest = dict(rest_t)
        return PLFunction([*rest.items()])
    elif request.param == "short_max":
        *rest_t, _ = aft_zfw_dict.items()
        rest = dict(rest_t)
        return PLFunction([*rest.items()])
    else:
        raise ValueError("invalid_aft_line internal fault")


@pytest.fixture
def good_idx() -> CG:
    return CG(29.84, 17841)


@pytest.fixture
def bad_fwd_idx() -> CG:
    return CG(33, 14500)


@pytest.fixture
def bad_aft_idx() -> CG:
    return CG(59, 15400)


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


def test_intersecting_lines():
    with pytest.raises(ValueError, match="fwd_line and aft_line should not overlap"):
        CGLimits(PLFunction([(0, 0), (10, 10)]), PLFunction([(0, 10), (10, 0)]))


def test_good_idx(zfw_cglimits, good_idx):
    assert good_idx in zfw_cglimits


def test_bad_fwd_idx(zfw_cglimits, bad_fwd_idx):
    assert bad_fwd_idx not in zfw_cglimits


def test_bad_aft_idx(zfw_cglimits, bad_aft_idx):
    assert bad_aft_idx not in zfw_cglimits
