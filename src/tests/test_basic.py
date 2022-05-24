import pytest
from crjwb.basic import BasicCalc, Interpolable


@pytest.fixture(scope="module")
def basic_calc() -> BasicCalc:
    """
    Get BasicCalc with following parameters:

    REF_STATION = 13.2

    K_CONSTANT = 50

    C_CONSTANT = 280

    MACRC_LENGTH = 2.526

    LEMAC_AT = 12.542


    Yields:
        BasicCalc: BasicCalc
    """
    return BasicCalc(13.2, 50, 280, 2.526, 12.542)


@pytest.fixture(scope="module")
def interp() -> Interpolable:
    return Interpolable({1: 10, 2: 20, 3: 30, 40: 400, 50: -500})


@pytest.mark.parametrize(
    "basic_calc, idx, weight, mac",
    [
        ("basic_calc", 29.84, 17843, 13.52),
        ("basic_calc", 23.72, 21627, 12.58),
        ("basic_calc", 23.83, 20354, 11.80),
    ],
    indirect=["basic_calc"],
)
def test_calc_macrc(basic_calc, idx, weight, mac):
    """
    Compare BasicCalc.calc_macrc() calculations results with \
    real loadsheet data.
    """
    assert basic_calc.calc_macrc(idx, weight) == pytest.approx(mac, 1e-3)


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
