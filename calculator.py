"""
Weight and balance calculation module.
"""
from dataclasses import dataclass

from basic import calc_macrc
from fuel import TripInfo


@dataclass
class Aircraft:
    dow: int
    doi: float
    mzfw: int
    mtow: int
    mlw: int
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


class WBCalculationError(Exception):
    pass


class WBCalculator:
    def __init__(self, aircraft: Aircraft, weights: StandardWeights) -> None:
        self.aircraft = aircraft
        self.weights = weights

    def calculate(
        self,
        trip_info: TripInfo,
        payload: Payload,
    ):
        if payload.pax_a > aircraft.a_capacity:
            raise WBCalculationError(
                f"Number of PAX in area A ({payload.pax_a})"
                f"exceeds limit ({aircraft.a_capacity})."
            )
        if payload.pax_b > aircraft.b_capacity:
            raise WBCalculationError(
                f"Number of PAX in area B ({payload.pax_b})"
                f"exceeds limit ({aircraft.b_capacity})."
            )
        if payload.pax_c > aircraft.c_capacity:
            raise WBCalculationError(
                f"Number of PAX in area C ({payload.pax_c})"
                f"exceeds limit ({aircraft.c_capacity})."
            )
        if payload.pax_d > aircraft.d_capacity:
            raise WBCalculationError(
                f"Number of PAX in area D ({payload.pax_a})"
                f"exceeds limit ({aircraft.d_capacity})."
            )
        operating_weight = self.aircraft.dow + trip_info.takeoff_fuel
        allowed_tow = min(
            self.aircraft.mtow,
            self.aircraft.mzfw + trip_info.takeoff_fuel,
            self.aircraft.mlw + trip_info.trip_fuel,
        )
        allowed_traffic_load = allowed_tow - operating_weight
        if allowed_traffic_load < 0:
            raise WBCalculationError("Allowed traffic load is below zero.")
        total_traffic_load = (
            payload.adults * self.weights.adult
            + payload.children * self.weights.child
            + payload.infants * self.weights.infant
            + payload.cabin_baggage
            + payload.cargo
        )
        # TODO: check for negative value
        underload_lmc = allowed_traffic_load - total_traffic_load
        if underload_lmc < 0:
            raise WBCalculationError(
                f"Total traffic load ({total_traffic_load}) exceeds "
                f"allowed traffic load ({allowed_traffic_load})."
            )
        zfw = self.aircraft.dow + total_traffic_load
        tow = zfw + trip_info.takeoff_fuel
        ldw = tow - trip_info.trip_fuel
        lizfw = (
            self.aircraft.doi
            + payload.cargo * self.aircraft.cargo_influence
            + payload.pax_a * self.weights.adult * self.aircraft.a_influence
            + payload.pax_b * self.weights.adult * self.aircraft.b_influence
            + payload.pax_c * self.weights.adult * self.aircraft.c_influence
            + payload.pax_d * self.weights.adult * self.aircraft.d_influence
        )
        litow = lizfw + trip_info.takeoff_fuel_index
        lilaw = lizfw + trip_info.landing_fuel_index
        maczfw = calc_macrc(lizfw, zfw)
        mactow = calc_macrc(litow, tow)
        macldw = calc_macrc(lilaw, ldw)
        print(
            f"LIZFW {round(lizfw, 2)}\nLITOW {round(litow, 2)}\n"
            f"LILAW {round(lilaw, 2)}\n"
            f"MACZFW {round(maczfw, 2)}\nMACTOW {round(mactow, 2)}\n"
            f"MACLDW {round(macldw, 2)}"
        )


if __name__ == "__main__":
    # should be fetched from db
    aircraft = Aircraft(
        dow=14434,
        doi=49.81,
        mzfw=19958,
        mtow=24040,
        mlw=21319,
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
    weights = StandardWeights(adult=75, child=30, infant=15)
    trip_info = TripInfo(3786, 1771)
    payload_data = Payload(
        adults=41,
        children=2,
        infants=0,
        cabin_baggage=91,
        cargo=181,
        pax_a=12,
        pax_b=12,
        pax_c=9,
        pax_d=10,
    )
    calc = WBCalculator(aircraft, weights)
    calc.calculate(trip_info, payload_data)
