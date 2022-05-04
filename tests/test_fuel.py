import pytest
from crjwb.fuel import get_closest_fuel_index


def test_negative_fuel():
    with pytest.raises(ValueError):
        get_closest_fuel_index(-1)


def test_fuel_exceeds_maximum():
    with pytest.raises(ValueError):
        get_closest_fuel_index(6500)


def test_exact_fuel_key():
    assert get_closest_fuel_index(200) == -0.83


def test_return_less():
    assert get_closest_fuel_index(3250) == -6.31


def test_return_more():
    assert get_closest_fuel_index(3350) == -6.27


def test_equidistant_fuel_returns_greater_influence():
    assert get_closest_fuel_index(3300) == -6.31
