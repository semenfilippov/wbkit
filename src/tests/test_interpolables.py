import pytest
from crjwb.interpolables import FuelEffect, Interpolable, Stab


@pytest.fixture(scope="module")
def interp() -> Interpolable:
    return Interpolable({1: 10, 2: 20, 3: 30, 40: 400, 50: -500})


def test_interp_one_point_raises():
    with pytest.raises(ValueError):
        Interpolable({1: 10})


def test_range_validation_does_not_raise(interp: Interpolable):
    interp.__validate_in_range__(1.5)


def test_range_validation_lt_min_raises(interp: Interpolable):
    with pytest.raises(ValueError):
        interp.__validate_in_range__(0.9)


def test_range_validation_gt_max_raises(interp: Interpolable):
    with pytest.raises(ValueError):
        interp.__validate_in_range__(51)


def test_interp_lt_min_raises(interp: Interpolable):
    with pytest.raises(ValueError):
        interp.get_interpolated_value(0.5)


def test_interp_gt_max_raises(interp: Interpolable):
    with pytest.raises(ValueError):
        interp.get_interpolated_value(51)


def test_interpolate_value(interp: Interpolable):
    assert interp.get_interpolated_value(1.5) == 15


def test_defined_lt_min_raises(interp: Interpolable):
    with pytest.raises(ValueError):
        interp.get_defined_value(0)


def test_defined_gt_max_raises(interp: Interpolable):
    with pytest.raises(ValueError):
        interp.get_defined_value(51)


def test_defined_less(interp: Interpolable):
    assert interp.get_defined_value(44) == 400


def test_defined_greater(interp: Interpolable):
    assert interp.get_defined_value(46) == -500


def test_defined_equidistant(interp: Interpolable):
    assert interp.get_defined_value(45) == -500


# TODO: PYTEST CLASS
# FROM test_fuel.py


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
    return FuelEffect(fe_dict)


def test_empty_dict():
    with pytest.raises(ValueError):
        FuelEffect({})


def test_get_min(fe_obj: FuelEffect):
    assert fe_obj.get_min() == 200


def test_get_max(fe_obj: FuelEffect):
    assert fe_obj.get_max() == 6488


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


# TODO: PYTEST CLASS
# FROM test_stab.py


@pytest.fixture(scope="module")
def stab():
    yield Stab({8.8: 8.15, 35: 4})


def test_one_point():
    with pytest.raises(ValueError):
        Stab({1.1: 2.1})


def test_exceeds_fwd_limit(stab: Stab):
    with pytest.raises(ValueError):
        stab.calc(8)


def test_exceeds_aft_limit(stab: Stab):
    with pytest.raises(ValueError):
        stab.calc(36)


def test_calc(stab: Stab):
    assert round(stab.calc(12.58), 2) == 7.55


def test_calc_stab_fwd_limit(stab: Stab):
    assert round(stab.calc(8.8), 2) == 8.15


def test_calc_stab_aft_limit(stab: Stab):
    assert round(stab.calc(35), 2) == 4
