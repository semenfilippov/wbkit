import pytest
from crjwb.calculator import CalculationResult, calculate_wb
from crjwb.exceptions import (
    AftMACLimitsViolatedError,
    ForwardMACLimitsViolatedError,
    IncorrectTripFuelError,
    NotEnoughSeatsOccupiedError,
    PayloadTooHeavyError,
    TooManySeatsOccupiedError,
)
from crjwb.inputclasses import AircraftData, CalculationTask, StandardWeights
from crjwb.stab import eicas_round

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

WEIGHTS = StandardWeights(75, 30, 15)

TASK_WRONG_FUEL = CalculationTask(takeoff_fuel=3300, trip_fuel=3500)

TASK_NOT_ENOUGH_SEATS_OCCUPIED = CalculationTask(
    num_adults=10, num_children=10, num_infants=10, pax_a=4, pax_b=4, pax_c=4, pax_d=4
)

TASK_TOO_MUCH_SEATS_OCCUPIED = CalculationTask(
    num_adults=10, num_children=10, num_infants=10, pax_a=7, pax_b=7, pax_c=7, pax_d=7
)

TASK_PAYLOAD_TOO_HEAVY = CalculationTask(6086, 3500, 50, 0, 0, 200, 16, 12, 12, 10, 800)

TASK_REAL = CalculationTask(3786, 1273, 41, 2, 0, 91, 12, 12, 9, 10, 181)

EXPECTED_CALC_RESULT = CalculationResult(
    AIRCRAFT_DATA,
    TASK_REAL,
    WEIGHTS,
    18220,
    22592,
    4372,
    3407,
    965,
    17841,
    21627,
    20354,
    29.84,
    23.72,
    23.83,
    13.52,
    12.58,
    11.80,
    7.5,
    0,
)

TASK_EXCEEDS_FWD_MAC = CalculationTask(5800, 2800, 16, 0, 0, 100, 16)

TASK_EXCEEDS_AFT_MAC = CalculationTask(3000, 1000, 10, pax_d=10, cargo=1200)

TASK_EXCEEDS_FWD_ALLOW_BALLAST = TASK_EXCEEDS_FWD_MAC._replace(allow_ballast=True)


def test_incorrect_fuel():
    with pytest.raises(IncorrectTripFuelError):
        calculate_wb(AIRCRAFT_DATA, WEIGHTS, TASK_WRONG_FUEL)


def test_not_enough_seats_occupied():
    with pytest.raises(NotEnoughSeatsOccupiedError):
        calculate_wb(AIRCRAFT_DATA, WEIGHTS, TASK_NOT_ENOUGH_SEATS_OCCUPIED)


def test_too_much_seats_occupied():
    with pytest.raises(TooManySeatsOccupiedError):
        calculate_wb(AIRCRAFT_DATA, WEIGHTS, TASK_TOO_MUCH_SEATS_OCCUPIED)


def test_payload_too_heavy():
    with pytest.raises(PayloadTooHeavyError):
        calculate_wb(AIRCRAFT_DATA, WEIGHTS, TASK_PAYLOAD_TOO_HEAVY)


def test_calculation_result():
    result = calculate_wb(AIRCRAFT_DATA, WEIGHTS, TASK_REAL)
    assert result.aircraft == EXPECTED_CALC_RESULT.aircraft
    assert result.task == EXPECTED_CALC_RESULT.task
    assert result.weights == EXPECTED_CALC_RESULT.weights
    assert result.operating_weight == EXPECTED_CALC_RESULT.operating_weight
    assert result.allowed_tow == EXPECTED_CALC_RESULT.allowed_tow
    assert result.allowed_payload == EXPECTED_CALC_RESULT.allowed_payload
    assert result.payload == EXPECTED_CALC_RESULT.payload
    assert result.underload_lmc == EXPECTED_CALC_RESULT.underload_lmc
    assert result.zfw == EXPECTED_CALC_RESULT.zfw
    assert result.tow == EXPECTED_CALC_RESULT.tow
    assert result.ldw == EXPECTED_CALC_RESULT.ldw
    assert abs(result.lizfw - EXPECTED_CALC_RESULT.lizfw) < 1
    assert abs(result.litow - EXPECTED_CALC_RESULT.litow) < 1
    assert abs(result.lilaw - EXPECTED_CALC_RESULT.lilaw) < 1
    assert abs(result.mactow - EXPECTED_CALC_RESULT.mactow) < 1
    assert abs(result.maczfw - EXPECTED_CALC_RESULT.maczfw) < 1
    assert abs(result.maclaw - EXPECTED_CALC_RESULT.maclaw) < 1
    assert abs(result.stab_trim - EXPECTED_CALC_RESULT.stab_trim) < 0.2
    assert eicas_round(result.stab_trim) == eicas_round(EXPECTED_CALC_RESULT.stab_trim)
    assert result.required_ballast == EXPECTED_CALC_RESULT.required_ballast


def test_raises_fwd_mac_limits():
    with pytest.raises(ForwardMACLimitsViolatedError):
        calculate_wb(AIRCRAFT_DATA, WEIGHTS, TASK_EXCEEDS_FWD_MAC)


def test_raises_aft_mac_limits():
    with pytest.raises(AftMACLimitsViolatedError):
        calculate_wb(AIRCRAFT_DATA, WEIGHTS, TASK_EXCEEDS_AFT_MAC)


def test_calc_allow_ballast():
    result = calculate_wb(AIRCRAFT_DATA, WEIGHTS, TASK_EXCEEDS_FWD_ALLOW_BALLAST)
    assert result.required_ballast > 0
