from dataclasses import dataclass


@dataclass
class Aircraft:
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
class Payload:
    adults: int
    children: int
    infants: int
    cabin_baggage: int
    cargo: int
    pax_a: int
    pax_b: int
    pax_c: int
    pax_d: int


@dataclass
class StandardWeights:
    adult: int
    child: int
    infant: int
