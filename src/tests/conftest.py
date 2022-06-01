import pytest

from wbkit.basic import WBConstants
from wbkit.cglimits import CGLimits
from wbkit.interpolables import Interpolable


# REF_ST, C, K


@pytest.fixture(scope="module")
def ref_st() -> float:
    return 13.2


@pytest.fixture(scope="module")
def c() -> int:
    return 280


@pytest.fixture(scope="module")
def k() -> int:
    return 50


@pytest.fixture(scope="module")
def macrc_length() -> float:
    return 2.526


@pytest.fixture(scope="module")
def lemac_at() -> float:
    return 12.542


@pytest.fixture
def rck(
    ref_st: float, c: int, k: int, macrc_length: float, lemac_at: float
) -> WBConstants:
    return WBConstants(ref_st, c, k, macrc_length, lemac_at)


# STAB


def stab() -> Interpolable:
    return Interpolable([(8.8, 8.15), (35, 4)])


# FUEL


def fuel() -> Interpolable:
    fuel_dict = {
        200: -0.83,
        400: -1.56,
        600: -2.22,
        800: -2.83,
        1000: -3.40,
        1200: -3.92,
        1400: -4.39,
        1600: -4.81,
        1800: -5.17,
        2000: -5.47,
        2200: -5.73,
        2400: -5.93,
        2600: -6.07,
        2800: -6.21,
        3000: -6.32,
        3200: -6.31,
        3400: -6.27,
        3600: -6.27,
        3800: -6.11,
        4000: -6.02,
        4200: -5.60,
        4255: -5.47,
        4400: -6.30,
        4600: -7.38,
        4800: -8.40,
        5000: -9.44,
        5200: -10.56,
        5400: -11.56,
        5600: -12.63,
        5800: -13.69,
        6000: -14.82,
        6200: -15.98,
        6400: -17.28,
        6488: -17.91,
    }
    return Interpolable([*fuel_dict.items()])


# CG LIMITS
# ZFW


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
def zfw_fwd_line(fwd_zfw_dict) -> Interpolable:
    return Interpolable([*fwd_zfw_dict.items()])


@pytest.fixture
def zfw_aft_line(aft_zfw_dict) -> Interpolable:
    return Interpolable([*aft_zfw_dict.items()])


@pytest.fixture
def zfw_cglimits(zfw_fwd_line, zfw_aft_line) -> CGLimits:
    return CGLimits(zfw_fwd_line, zfw_aft_line)


# TOW


@pytest.fixture
def tow_fwd_line() -> Interpolable:
    tow_fwd = {
        13608: 34.45,
        14515: 33.22,
        16329: 24.92,
        23133: 14.47,
        24040: 13.08,
    }
    return Interpolable([*tow_fwd.items()])


@pytest.fixture
def tow_aft_line() -> Interpolable:
    tow_aft = {
        13608: 57.31,
        15422: 58.28,
        16329: 63.19,
        23133: 68.68,
        23521: 68.99,
        24040: 49.89,
    }
    return Interpolable([*tow_aft.items()])


@pytest.fixture
def tow_cglimits(tow_fwd_line, tow_aft_line):
    return CGLimits(tow_fwd_line, tow_aft_line)


# INFLIGHT


@pytest.fixture
def infl_fwd_line() -> Interpolable:
    infl_fwd = {
        13608: 31.53,
        15422: 29.06,
        17237: 20.38,
        23133: 10.25,
        24040: 8.69,
    }
    return Interpolable([*infl_fwd.items()])


@pytest.fixture
def infl_aft_line() -> Interpolable:
    infl_aft = {
        13608: 57.31,
        15422: 58.28,
        16933: 66.73,
        23133: 72.85,
        23406: 73.12,
        24040: 49.89,
    }
    return Interpolable([*infl_aft.items()])


@pytest.fixture
def infl_cglimits(infl_fwd_line, infl_aft_line) -> CGLimits:
    return CGLimits(infl_fwd_line, infl_aft_line)


# LANDING


@pytest.fixture
def ldg_fwd_line():
    ldg_fwd = {
        13608: 34.45,
        14515: 33.22,
        16329: 24.92,
        21319: 17.21,
    }
    return Interpolable([*ldg_fwd.items()])


@pytest.fixture
def ldg_aft_line():
    ldg_aft = {
        13608: 57.31,
        15422: 58.28,
        16329: 63.19,
        21319: 67.22,
    }
    return Interpolable([*ldg_aft.items()])


@pytest.fixture
def ldg_cglimits(ldg_fwd_line, ldg_aft_line) -> CGLimits:
    return CGLimits(ldg_fwd_line, ldg_aft_line)
