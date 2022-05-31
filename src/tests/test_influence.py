import pytest
from wbkit.basic import Index, IndexInfluence


@pytest.fixture
def idx_infl(rck) -> IndexInfluence:
    return IndexInfluence(-1, rck)


def test_init(idx_infl: IndexInfluence, rck):
    assert idx_infl.__influence__ == Index(-1, 1, rck)


def test_mul(idx_infl: IndexInfluence, rck):
    assert idx_infl * 10 == Index(-10, 10, rck)


def test_get_idx(idx_infl: IndexInfluence, rck):
    assert idx_infl.get_idx(10) == Index(-10, 10, rck)
