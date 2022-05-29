from typing import Tuple
import pytest
from wbkit.basic import Index, IndexInfluence, PercentMAC


@pytest.fixture(scope="module")
def ref_st() -> float:
    return 13.2


@pytest.fixture(scope="module")
def c() -> int:
    return 280


@pytest.fixture(scope="module")
def k() -> int:
    return 50


@pytest.fixture
def rck(ref_st: float, c: int, k: int) -> Tuple[float, int, int]:
    return ref_st, c, k


@pytest.fixture(scope="module")
def macrc_length() -> float:
    return 2.526


@pytest.fixture(scope="module")
def lemac_at() -> float:
    return 12.542


class TestIndex:
    @staticmethod
    def test_init(ref_st: float, c: int, k: int):
        idx = Index(50, 14500, ref_st, c, k)
        assert idx.value == 50
        assert idx.weight == 14500
        assert idx.ref_st == ref_st
        assert idx.c == c
        assert idx.k == k

    @staticmethod
    @pytest.mark.parametrize(["c"], [(0,), (-1,)])
    def test_init_c_le_zero_raises(c):
        with pytest.raises(ValueError, match="C constant should be greater than 0"):
            Index(50, 14500, 10.0, c, 50)

    @staticmethod
    def test_init_negative_k_raises():
        with pytest.raises(ValueError, match="K constant should not be negative"):
            Index(50, 14500, 10.0, 1, -1)

    @staticmethod
    def test_init_negative_weight_raises():
        with pytest.raises(ValueError, match="weight should not be negative"):
            Index(50, -1, 10.0, 1, 1)

    @staticmethod
    def test_from_moment():
        idx = Index.from_moment(10, 10, 0, 2, 10)
        assert idx.value == 15

    @staticmethod
    @pytest.mark.parametrize(
        ["idx_value", "weight", "c", "k"], [(10, 10, 1, 0), (48.5, 14500, 280, 50)]
    )
    def test_moment_property(idx_value: float, weight: int, c: int, k: int):
        idx = Index(idx_value, weight, 14.0, c, k)
        assert idx.moment == (idx_value - k) * c

    @staticmethod
    def test_calc():
        idx = Index.calc(100, 10, 0, 2, 50)
        assert idx.value == 550
        assert idx.moment == 1000

    @staticmethod
    @pytest.mark.parametrize(["ref_st", "c", "k"], [(5, 1, 0), (10, 2, 0), (10, 1, 2)])
    def test_validate_calc_ops_raises(rck):
        a = Index(10, 10, 10, 1, 0)
        b = Index(10, 10, *rck)
        with pytest.raises(
            ValueError,
            match="Calculations for Index operands with different "
            "reference stations, C or K constants are not allowed.",
        ):
            a.__validate_calc_ops__(b)

    @staticmethod
    def test_validate_calc_ops_does_not_raise():
        a = Index(5, 20, 10, 1, 0)
        b = Index(2, 30, 10, 1, 0)
        a.__validate_calc_ops__(b)

    @staticmethod
    def test_validate_comp_ops_raises():
        a = Index(5, 20, 9, 1, 0)
        b = Index(2, 30, 10, 1, 0)
        with pytest.raises(
            ValueError,
            match="Cannot compare Index instances with different reference stations.",
        ):
            a.__validate_compare_ops__(b)

    @staticmethod
    def test_validate_comp_ops_does_not_raise():
        a = Index(5, 20, 10, 1, 0)
        b = Index(2, 30, 10, 1, 0)
        a.__validate_compare_ops__(b)

    @staticmethod
    def test_add():
        a = Index(5, 20, 10, 1, 0)
        b = Index(2, 30, 10, 1, 0)
        c = a + b
        assert c.value == a.value + b.value
        assert c.weight == a.weight + b.weight

    @staticmethod
    def test_sub():
        a = Index(5, 40, 10, 1, 0)
        b = Index(2, 30, 10, 1, 0)
        c = a - b
        assert c.value == a.value - b.value
        assert c.weight == a.weight - b.weight

    @staticmethod
    def test_mul(ref_st: float, c: int, k: int):
        idx = Index(-1, 1, ref_st, c, k)
        assert idx * 10 == Index(-10, 10, ref_st, c, k)

    @staticmethod
    def test_eq():
        a = Index(5, 20, 10, 1, 0)
        b = Index(5, 20, 10, 1, 0)
        assert a == b

    @staticmethod
    def test_gt():
        a = Index(10, 20, 30, 1, 0)
        b = Index(9, 20, 30, 1, 0)
        assert a > b

    @staticmethod
    def test_lt():
        a = Index(9, 20, 30, 1, 0)
        b = Index(10, 20, 30, 1, 0)
        assert a < b

    @staticmethod
    def test_ge():
        a = Index(10, 20, 30, 1, 0)
        b = Index(10, 20, 30, 1, 0)
        c = Index(9, 20, 30, 1, 0)
        assert a >= b
        assert a >= c

    @staticmethod
    def test_le():
        a = Index(10, 20, 30, 1, 0)
        b = Index(10, 20, 30, 1, 0)
        c = Index(11, 20, 30, 1, 0)
        assert a <= b
        assert a <= c


@pytest.fixture
def idx_infl(rck) -> IndexInfluence:
    return IndexInfluence(-1, *rck)


class TestIndexInfluence:
    @staticmethod
    def test_init(idx_infl: IndexInfluence, rck):
        assert idx_infl.__influence__ == Index(-1, 1, *rck)

    @staticmethod
    def test_mul(idx_infl: IndexInfluence, rck):
        assert idx_infl * 10 == Index(-10, 10, *rck)

    @staticmethod
    def test_get_idx(idx_infl: IndexInfluence, rck):
        assert idx_infl.get_idx(10) == Index(-10, 10, *rck)


# PercentMAC tests


class TestPercentMAC:
    @staticmethod
    def test_init(lemac_at: float, macrc_length: float):
        pctmac = PercentMAC(13.52, lemac_at, macrc_length)
        assert pctmac.value == 13.52
        assert pctmac.lemac_at == lemac_at
        assert pctmac.macrc_length == macrc_length

    @staticmethod
    @pytest.mark.parametrize(
        [
            "idx_value",
            "weight",
            "pctmac_value",
            "ref_st",
            "c",
            "k",
            "lemac_at",
            "macrc_length",
        ],
        [
            (61.84, 14007, 35.42, "ref_st", "c", "k", "lemac_at", "macrc_length"),
            (49.81, 14434, 25.90, "ref_st", "c", "k", "lemac_at", "macrc_length"),
            (29.84, 17841, 13.52, "ref_st", "c", "k", "lemac_at", "macrc_length"),
            (23.72, 21627, 12.58, "ref_st", "c", "k", "lemac_at", "macrc_length"),
            (23.83, 20354, 11.80, "ref_st", "c", "k", "lemac_at", "macrc_length"),
        ],
        indirect=["ref_st", "c", "k", "lemac_at", "macrc_length"],
    )
    def test_from_idx(
        idx_value: float,
        weight: int,
        pctmac_value: float,
        ref_st: float,
        c: int,
        k: int,
        lemac_at: float,
        macrc_length: float,
    ):
        idx = Index(idx_value, weight, ref_st, c, k)
        pctmac = PercentMAC.from_idx(idx, lemac_at, macrc_length)
        assert pctmac.value == pytest.approx(pctmac_value, 1e-3)
        assert pctmac.lemac_at == lemac_at
        assert pctmac.macrc_length == macrc_length

    @staticmethod
    @pytest.mark.parametrize(
        [
            "idx_value",
            "weight",
            "pctmac_value",
            "ref_st",
            "c",
            "k",
            "lemac_at",
            "macrc_length",
        ],
        [
            (29.84, 17841, 13.52, "ref_st", "c", "k", "lemac_at", "macrc_length"),
            (23.72, 21627, 12.58, "ref_st", "c", "k", "lemac_at", "macrc_length"),
            (23.83, 20354, 11.80, "ref_st", "c", "k", "lemac_at", "macrc_length"),
        ],
        indirect=["ref_st", "c", "k", "lemac_at", "macrc_length"],
    )
    def test_to_idx(
        idx_value: float,
        weight: int,
        pctmac_value: float,
        ref_st: float,
        c: int,
        k: int,
        lemac_at: float,
        macrc_length: float,
    ):
        pctmac = PercentMAC(pctmac_value, lemac_at, macrc_length)
        exp_idx = Index(idx_value, weight, ref_st, c, k)
        idx = pctmac.to_idx(weight, ref_st, c, k)
        assert idx.value == pytest.approx(exp_idx.value, 1e-3)
        assert idx.weight == exp_idx.weight
        assert idx.ref_st == exp_idx.ref_st
        assert idx.c == exp_idx.c
        assert idx.k == exp_idx.k
