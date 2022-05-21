import pytest
from crjwb.fuel import FuelEffect


@pytest.fixture(scope="module")
def fe_dict() -> dict:
    return {
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


@pytest.fixture(scope="module")
def fe_obj(fe_dict: dict) -> FuelEffect:
    yield FuelEffect(fe_dict)


def test_empty_dict():
    with pytest.raises(ValueError):
        FuelEffect({})


def test_get_min(fe_obj: FuelEffect):
    assert fe_obj.get_min_fuel() == 200


def test_get_max(fe_obj: FuelEffect):
    assert fe_obj.get_max_fuel() == 6488


def test_get_less_than_min(fe_obj: FuelEffect):
    with pytest.raises(ValueError):
        fe_obj.get_influence(100)


def test_get_greater_than_max(fe_obj: FuelEffect):
    with pytest.raises(ValueError):
        fe_obj.get_influence(6500)


def test_get_exact(fe_obj: FuelEffect):
    assert fe_obj.get_influence(3000) == -6.32


def test_get_approx_less(fe_obj: FuelEffect):
    assert fe_obj.get_influence(6299) == -15.98


def test_get_approx_greater(fe_obj: FuelEffect):
    assert fe_obj.get_influence(6301) == -17.28


def test_get_equidistant(fe_obj: FuelEffect):
    assert fe_obj.get_influence(6300) == -17.28
