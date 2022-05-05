import pytest
from crjwb.cabinareatrim import calc_pax_influence, calc_pax_weight
from crjwb.inputclasses import StandardWeights

WEIGHTS = StandardWeights(75, 30, 15)
NUM_ADULTS = 41
NUM_CHILDREN = 2
NUM_INFANTS = 0
CABIN_BAGGAGE = 91
A_INFLUENCE = -0.01997
B_INFLUENCE = -0.01013
C_INFLUENCE = -0.00161
D_INFLUENCE = 0.00627
A_PAX = 12
B_PAX = 12
C_PAX = 9
D_PAX = 10
REAL_PAX_INFLUENCE = -(49.81 + 181 * 0.01547 - 29.84)


def test_calc_pax_weight():
    assert (
        calc_pax_weight(
            WEIGHTS,
            NUM_ADULTS,
            NUM_CHILDREN,
            NUM_INFANTS,
            CABIN_BAGGAGE,
        )
        == 3226
    )


def test_calc_pax_influence():
    assert calc_pax_influence(
        WEIGHTS,
        A_INFLUENCE,
        B_INFLUENCE,
        C_INFLUENCE,
        D_INFLUENCE,
        A_PAX,
        B_PAX,
        C_PAX,
        D_PAX,
    ) == pytest.approx(-23.474, 1e-3)


def test_compare_to_real_calculation():
    assert (
        abs(
            calc_pax_influence(
                WEIGHTS,
                A_INFLUENCE,
                B_INFLUENCE,
                C_INFLUENCE,
                D_INFLUENCE,
                A_PAX,
                B_PAX,
                C_PAX,
                D_PAX,
            )
            - REAL_PAX_INFLUENCE
        )
        < 1
    )
