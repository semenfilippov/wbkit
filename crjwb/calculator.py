from dataclasses import dataclass

from .basic import calc_macrc
from .fuel import TripInfo, get_closest_fuel_index
from .inputclasses import Aircraft, Payload, StandardWeights
from .stab import calc_stab


@dataclass
class CalculationResult:
    operating_weight: int
    allowed_tow: int
    allowed_traffic_load: int
    total_traffic_load: int
    underload_before_lmc: int
    mzfw: int
    mtow: int
    mldw: int
    zfw: int
    tow: int
    ldw: int
    lizfw: float
    litow: float
    lilaw: float
    maczfw: float
    mactow: float
    maclaw: float
    stab_trim: float


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
    ) -> CalculationResult:
        if payload.pax_a > self.aircraft.a_capacity:
            raise WBCalculationError(
                f"Number of PAX in area A ({payload.pax_a})"
                f"exceeds limit ({self.aircraft.a_capacity})."
            )
        if payload.pax_b > self.aircraft.b_capacity:
            raise WBCalculationError(
                f"Number of PAX in area B ({payload.pax_b})"
                f"exceeds limit ({self.aircraft.b_capacity})."
            )
        if payload.pax_c > self.aircraft.c_capacity:
            raise WBCalculationError(
                f"Number of PAX in area C ({payload.pax_c})"
                f"exceeds limit ({self.aircraft.c_capacity})."
            )
        if payload.pax_d > self.aircraft.d_capacity:
            raise WBCalculationError(
                f"Number of PAX in area D ({payload.pax_a})"
                f"exceeds limit ({self.aircraft.d_capacity})."
            )
        operating_weight = self.aircraft.dow + trip_info.takeoff_fuel
        allowed_tow = min(
            self.aircraft.mtow,
            self.aircraft.mzfw + trip_info.takeoff_fuel,
            self.aircraft.mldw + trip_info.trip_fuel,
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
        underload_before_lmc = allowed_traffic_load - total_traffic_load
        if underload_before_lmc < 0:
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
        litow = lizfw + get_closest_fuel_index(trip_info.takeoff_fuel)
        lilaw = lizfw + get_closest_fuel_index(trip_info.landing_fuel)
        maczfw = calc_macrc(lizfw, zfw)
        mactow = calc_macrc(litow, tow)
        maclaw = calc_macrc(lilaw, ldw)
        stab_trim = calc_stab(mactow, True)
        return CalculationResult(
            operating_weight,
            allowed_tow,
            allowed_traffic_load,
            total_traffic_load,
            underload_before_lmc,
            self.aircraft.mzfw,
            self.aircraft.mtow,
            self.aircraft.mldw,
            zfw,
            tow,
            ldw,
            lizfw,
            litow,
            lilaw,
            maczfw,
            mactow,
            maclaw,
            stab_trim,
        )
