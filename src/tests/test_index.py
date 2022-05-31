import pytest
from wbkit.basic import Index, IndexConstants


def test_init(rck):
    idx = Index(50, 14500, rck)
    assert idx.idx == 50
    assert idx.weight == 14500
    assert idx.rck == rck


def test_init_negative_weight_raises(rck):
    with pytest.raises(ValueError, match="weight should not be negative"):
        Index(50, -1, rck)


def test_from_moment():
    idx = Index.from_moment(10, 10, IndexConstants(0, 2, 10))
    assert idx.idx == 15


@pytest.mark.parametrize(
    ["idx_value", "weight", "c", "k"], [(10, 10, 1, 0), (48.5, 14500, 280, 50)]
)
def test_moment_property(idx_value: float, weight: int, c: int, k: int):
    idx = Index(idx_value, weight, IndexConstants(14.0, c, k))
    assert idx.moment == (idx_value - k) * c


def test_calc():
    idx = Index.calc(100, 10, IndexConstants(0, 2, 50))
    assert idx.idx == 550
    assert idx.moment == 1000


@pytest.mark.parametrize(["ref_st", "c", "k"], [(5, 1, 0), (10, 2, 0), (10, 1, 2)])
def test_validate_calc_ops_raises(ref_st, c, k):
    a = Index(10, 10, IndexConstants(10, 1, 0))
    b = Index(10, 10, IndexConstants(ref_st, c, k))
    with pytest.raises(
        ValueError,
        match="Calculations for Index operands with different "
        "reference stations, C or K constants are not allowed.",
    ):
        a.__validate_calc_ops__(b)


def test_validate_calc_ops_does_not_raise():
    a = Index(5, 20, IndexConstants(10, 1, 0))
    b = Index(2, 30, IndexConstants(10, 1, 0))
    a.__validate_calc_ops__(b)


def test_validate_comp_ops_raises():
    a = Index(5, 20, IndexConstants(9, 1, 0))
    b = Index(2, 30, IndexConstants(10, 1, 0))
    with pytest.raises(
        ValueError,
        match="Cannot compare Index instances with different reference stations.",
    ):
        a.__validate_compare_ops__(b)


def test_validate_comp_ops_does_not_raise():
    a = Index(5, 20, IndexConstants(10, 1, 0))
    b = Index(2, 30, IndexConstants(10, 1, 0))
    a.__validate_compare_ops__(b)


def test_add():
    a = Index(5, 20, IndexConstants(10, 1, 0))
    b = Index(2, 30, IndexConstants(10, 1, 0))
    c = a + b
    assert c.idx == a.idx + b.idx
    assert c.weight == a.weight + b.weight


def test_sub():
    a = Index(5, 40, IndexConstants(10, 1, 0))
    b = Index(2, 30, IndexConstants(10, 1, 0))
    c = a - b
    assert c.idx == a.idx - b.idx
    assert c.weight == a.weight - b.weight


def test_mul(rck: IndexConstants):
    idx = Index(-1, 1, rck)
    assert idx * 10 == Index(-10, 10, rck)


def test_rmul(rck: IndexConstants):
    idx = Index(-1, 1, rck)
    assert 10 * idx == Index(-10, 10, rck)


def test_eq(rck):
    a = Index(5, 20, rck)
    b = Index(5, 20, rck)
    assert a == b


def test_gt(rck):
    a = Index(10, 20, rck)
    b = Index(9, 20, rck)
    assert a > b


def test_lt(rck):
    a = Index(9, 20, rck)
    b = Index(10, 20, rck)
    assert a < b


def test_ge(rck):
    a = Index(10, 20, rck)
    b = Index(10, 20, rck)
    c = Index(9, 20, rck)
    assert a >= b
    assert a >= c


def test_le(rck):
    a = Index(10, 20, rck)
    b = Index(10, 20, rck)
    c = Index(11, 20, rck)
    assert a <= b
    assert a <= c
