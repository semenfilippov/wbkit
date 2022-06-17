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
def good_idx(zfw_cglimits: CGLimits) -> CG:
    return CG(29.84, 17841, zfw_cglimits)


@pytest.fixture
def bad_weight_idx(good_idx: CG):
    return good_idx._replace(weight=20000)


@pytest.fixture
def bad_fwd_idx(zfw_cglimits: CGLimits) -> CG:
    return CG(33, 14500, zfw_cglimits)


@pytest.fixture
def bad_aft_idx(zfw_cglimits: CGLimits) -> CG:
    return CG(59, 15400, zfw_cglimits)
