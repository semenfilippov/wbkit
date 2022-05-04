import pytest
from crjwb.cabinareatrim import calc_pax_influence, calc_pax_weight

AVG_ADULT_WEIGHT = 75
AVG_CHILD_WEIGHT = 30
AVG_INFANT_WEIGHT = 15
NUM_ADULTS = 40
NUM_CHILDREN = 2
NUM_INFANTS = 1
CABIN_BAGGAGE = 150
A_INFLUENCE = -0.01997
B_INFLUENCE = -0.01013
C_INFLUENCE = -0.00161
D_INFLUENCE = 0.00627
A_PAX = 11
B_PAX = 11
C_PAX = 10
D_PAX = 10


def test_calc_pax_weight():
    assert (
        calc_pax_weight(
            AVG_ADULT_WEIGHT,
            AVG_CHILD_WEIGHT,
            AVG_INFANT_WEIGHT,
            NUM_ADULTS,
            NUM_CHILDREN,
            NUM_INFANTS,
            CABIN_BAGGAGE,
        )
        == 3225
    )


def test_calc_pax_influence():
    assert calc_pax_influence(
        AVG_ADULT_WEIGHT,
        A_INFLUENCE,
        B_INFLUENCE,
        C_INFLUENCE,
        D_INFLUENCE,
        A_PAX,
        B_PAX,
        C_PAX,
        D_PAX,
    ) == pytest.approx(-21.3375, 1e-4)
