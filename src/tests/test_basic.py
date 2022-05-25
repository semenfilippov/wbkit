import pytest
from crjwb.basic import BasicCalc


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
