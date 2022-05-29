from typing import List, Tuple
import pytest
from wbkit.basic import Index, PercentMAC
from wbkit.cglimits import LimitLine


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
def idx_list(ref_st: float, c: int, k: int) -> List[Index]:
    return [
        Index(x, 13500 + n * 1000, ref_st, c, k)
        for n, x in enumerate(range(20, 70, 10))
    ]


@pytest.fixture
def pctmac_weight_pairs(
    idx_list: List[Index], macrc_length: float, lemac_at: float
) -> List[Tuple[int, PercentMAC]]:
    return [
        (x.weight, PercentMAC.from_idx(x, lemac_at, macrc_length)) for x in idx_list
    ]


@pytest.fixture(
    params=[(True, False, False), (False, True, False), (False, False, True)]
)
def invalid_idx_list(request, idx_list, ref_st, c, k):
    return idx_list + [
        Index(
            70,
            24000,
            999 if request.param[0] else ref_st,
            999 if request.param[1] else c,
            999 if request.param[2] else k,
        )
    ]


@pytest.fixture
def ll(idx_list) -> LimitLine:
    return LimitLine.from_idxs(idx_list)


class TestLimitLine:
    @staticmethod
    def test_init(ref_st: float, c: int, k: int):
        ll = LimitLine([(1, 2), (2, 3)], ref_st, c, k)
        assert ll.ref_st == ref_st
        assert ll.c == c
        assert ll.k == k

    @staticmethod
    def test_init_from_idxs(idx_list: List[Index], ref_st: float, c: int, k: int):
        ll = LimitLine.from_idxs(idx_list)
        assert ll.ref_st == ref_st
        assert ll.c == c
        assert ll.k == k

    @staticmethod
    def test_invalid_idx_seq_raises(invalid_idx_list: List[Index]):
        with pytest.raises(ValueError):
            LimitLine.from_idxs(invalid_idx_list)

    @staticmethod
    def test_init_from_pctmac_pairs(
        pctmac_weight_pairs: List[Tuple[int, PercentMAC]], ref_st: float, c: int, k: int
    ):
        ll = LimitLine.from_wght_pctmac_pairs(pctmac_weight_pairs, ref_st, c, k)
        assert ll.ref_st == ref_st
        assert ll.c == c
        assert ll.k == k

    @staticmethod
    def test_get_limit_idx(ll: LimitLine, ref_st: float, c: int, k: int):
        assert ll.get_limit_idx(13500) == Index(20, 13500, ref_st, c, k)
