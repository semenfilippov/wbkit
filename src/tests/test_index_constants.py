import pytest
from wbkit.basic import WBConstants


def test_eq():
    a = WBConstants(1, 1, 1, 1, 1)
    b = WBConstants(1, 1, 1, 1, 1)
    assert a == b


def test_hashable():
    a = WBConstants(1, 1, 1, 1, 1)
    b = WBConstants(1, 1, 1, 1, 1)
    assert a.__hash__() == b.__hash__()


def test_set():
    a = WBConstants(1, 1, 1, 1, 1)
    b = WBConstants(1, 1, 1, 1, 1)
    c = {a, b}
    assert len(c) == 1


def test_set_noneq():
    a = WBConstants(1, 1, 1, 1, 1)
    b = WBConstants(2, 1, 1, 1, 1)
    c = {a, b}
    assert len(c) == 2


@pytest.mark.parametrize(["c"], [(0,), (-1,)])
def test_init_c_le_zero_raises(c):
    with pytest.raises(ValueError, match="C constant should be greater than 0"):
        WBConstants(10.0, c, 50, 1, 1)


def test_init_negative_k_raises():
    with pytest.raises(ValueError, match="K constant should not be negative"):
        WBConstants(10.0, 1, -1, 1, 1)
