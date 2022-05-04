import pytest
from crjwb.calculator import calculate_wb
from crjwb.exceptions import (
    IncorrectTripFuelError,
    NotEnoughSeatsOccupiedError,
    PayloadTooHeavyError,
    TooManySeatsOccupiedError,
)
from crjwb.inputclasses import AircraftData, CalculationTask, StandardWeights

AIRCRAFT_DATA = AircraftData(
    dow=14434,
    doi=49.81,
    mzfw=19958,
    mtow=24040,
    mldw=21319,
    a_capacity=16,
    b_capacity=12,
    c_capacity=12,
    d_capacity=10,
    a_influence=-0.01997,
    b_influence=-0.01013,
    c_influence=-0.00161,
    d_influence=0.00627,
    cargo_influence=0.01547,
)

TASK_WRONG_FUEL = CalculationTask(takeoff_fuel=3300, trip_fuel=3500)

TASK_NOT_ENOUGH_SEATS_OCCUPIED = CalculationTask(
    num_adults=10, num_children=10, num_infants=10, pax_a=4, pax_b=4, pax_c=4, pax_d=4
)

TASK_TOO_MUCH_SEATS_OCCUPIED = CalculationTask(
    num_adults=10, num_children=10, num_infants=10, pax_a=7, pax_b=7, pax_c=7, pax_d=7
)

TASK_PAYLOAD_TOO_HEAVY = CalculationTask(6086, 3500, 50, 0, 0, 200, 16, 12, 12, 10, 800)


WEIGHTS = StandardWeights(75, 30, 15)


def test_incorrect_fuel():
    with pytest.raises(IncorrectTripFuelError):
        calculate_wb(AIRCRAFT_DATA, TASK_WRONG_FUEL, WEIGHTS)


def test_not_enough_seats_occupied():
    with pytest.raises(NotEnoughSeatsOccupiedError):
        calculate_wb(AIRCRAFT_DATA, TASK_NOT_ENOUGH_SEATS_OCCUPIED, WEIGHTS)


def test_too_much_seats_occupied():
    with pytest.raises(TooManySeatsOccupiedError):
        calculate_wb(AIRCRAFT_DATA, TASK_TOO_MUCH_SEATS_OCCUPIED, WEIGHTS)


def test_payload_too_heavy():
    with pytest.raises(PayloadTooHeavyError):
        calculate_wb(AIRCRAFT_DATA, TASK_PAYLOAD_TOO_HEAVY, WEIGHTS)
