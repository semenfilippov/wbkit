import pytest

from wbkit.basic import IndexConstants


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
def rck(ref_st: float, c: int, k: int) -> IndexConstants:
    return IndexConstants(ref_st, c, k)


@pytest.fixture(scope="module")
def macrc_length() -> float:
    return 2.526


@pytest.fixture(scope="module")
def lemac_at() -> float:
    return 12.542
