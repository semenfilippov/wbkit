from typing import List

import pytest
from wbkit.basic import Index, IndexConstants
from wbkit.cglimits import LimitLine, CGLimits


@pytest.fixture
def ref_st() -> float:
    return 13.2


@pytest.fixture
def c() -> int:
    return 280


@pytest.fixture
def k() -> int:
    return 50


@pytest.fixture
def rck(ref_st: float, c: int, k: int) -> IndexConstants:
    return IndexConstants(ref_st, c, k)


@pytest.fixture
def idx_list(rck: IndexConstants) -> List[Index]:
    return [Index(x, 13500 + n * 1000, rck) for n, x in enumerate(range(20, 70, 10))]


@pytest.fixture
def ll(idx_list: List[Index]) -> LimitLine:
    return LimitLine.from_idxs(idx_list)


@pytest.fixture(
    params=[(True, False, False), (False, True, False), (False, False, True)]
)
def invalid_idx_list(request, idx_list, ref_st: float, c: int, k: int) -> List[Index]:
    return idx_list + [
        Index(
            70,
            24000,
            IndexConstants(
                999 if request.param[0] else ref_st,
                999 if request.param[1] else c,
                999 if request.param[2] else k,
            ),
        )
    ]


@pytest.fixture
def fwd_line(rck) -> LimitLine:
    points = {
        13608: 34.45,
        14515: 33.22,
        15190: 30.14,
        19958: 22.82,
    }
    return LimitLine([(x[0], x[1]) for x in points.items()], rck)


@pytest.fixture
def aft_line(rck) -> LimitLine:
    points = {
        13608: 57.31,
        15422: 58.28,
        16329: 63.19,
        19958: 66.12,
    }
    return LimitLine([(x[0], x[1]) for x in points.items()], rck)


@pytest.fixture
def intersecting_lines(rck) -> List[LimitLine]:
    return [
        LimitLine([(0, 0), (10, 10)], rck),
        LimitLine([(10, 0), (0, 10)], rck),
    ]


@pytest.fixture
def valid_idx(rck) -> Index:
    return Index(50, 14500, rck)


@pytest.fixture
def violates_fwd_idx(rck) -> Index:
    return Index(33, 14500, rck)


@pytest.fixture
def violates_aft_idx(rck) -> Index:
    return Index(60, 15500, rck)


@pytest.fixture
def cglimits(rck, fwd_line, aft_line) -> CGLimits:
    cglimits = CGLimits(rck, [("Zero Fuel", fwd_line, aft_line)])
    return cglimits


class TestLimitLine:
    @staticmethod
    def test_init(rck: IndexConstants):
        ll = LimitLine([(1, 2), (2, 3)], rck)
        assert ll.rck == rck

    @staticmethod
    def test_from_idxs(idx_list: List[Index], rck: IndexConstants):
        ll = LimitLine.from_idxs(idx_list)
        assert ll.rck == rck

    @staticmethod
    def test_invalid_idx_seq_raises(invalid_idx_list: List[Index]):
        with pytest.raises(ValueError):
            LimitLine.from_idxs(invalid_idx_list)

    @staticmethod
    def test_get_limit_idx(ll: LimitLine, rck):
        assert ll.get_limit_idx(13500) == Index(20, 13500, rck)
