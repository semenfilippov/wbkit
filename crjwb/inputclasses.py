from dataclasses import dataclass


@dataclass
class AircraftData:
    dow: int
    doi: float
    mzfw: int
    mtow: int
    mldw: int
    a_capacity: int
    b_capacity: int
    c_capacity: int
    d_capacity: int
    a_influence: float
    b_influence: float
    c_influence: float
    d_influence: float
    cargo_influence: float


@dataclass
class CalculationTask:
    takeoff_fuel: int = 0
    trip_fuel: int = 0
    num_adults: int = 0
    num_children: int = 0
    num_infants: int = 0
    cabin_baggage: int = 0
    pax_a: int = 0
    pax_b: int = 0
    pax_c: int = 0
    pax_d: int = 0
    cargo: int = 0
    required_ballast: int = 0
    allow_ballast: bool = False


@dataclass
class StandardWeights:
    adult: int
    child: int
    infant: int
