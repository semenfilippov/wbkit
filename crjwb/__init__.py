"""
CRJ100/200 weight and balance calculation module.
"""
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

__all__ = [
    "CalculationResult",
    "calculate_wb",
    "AftMACLimitsViolatedError",
    "ForwardMACLimitsViolatedError",
    "IncorrectTripFuelError",
    "NotEnoughSeatsOccupiedError",
    "PayloadTooHeavyError",
    "TooManySeatsOccupiedError",
    "AircraftData",
    "CalculationTask",
    "StandardWeights",
]
