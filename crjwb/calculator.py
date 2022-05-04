from dataclasses import dataclass

from crjwb.basic import calc_macrc
from crjwb.cabinareatrim import calc_pax_influence, calc_pax_weight
from crjwb.exceptions import (
    IncorrectTripFuelError,
    NotEnoughSeatsOccupiedError,
    PayloadTooHeavyError,
    TooManySeatsOccupiedError,
)
from crjwb.fuel import get_closest_fuel_index
from crjwb.inputclasses import AircraftData, CalculationTask, StandardWeights
from crjwb.stab import calc_stab


@dataclass
class CalculationResult:
    aircraft: AircraftData
    task: CalculationTask
    weights: StandardWeights
    operating_weight: int
    allowed_weight_for_takeoff: int
    allowed_traffic_load: int
    underload_lmc: int
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


def calculate_wb(
    aircraft: AircraftData, task: CalculationTask, weights: StandardWeights
):
    if task.takeoff_fuel < task.trip_fuel:
        raise IncorrectTripFuelError(task.takeoff_fuel, task.trip_fuel)
    occupied_seats = task.pax_a + task.pax_b + task.pax_c + task.pax_d
    ttl_pax = task.num_adults + task.num_children
    if occupied_seats > ttl_pax:
        raise TooManySeatsOccupiedError(occupied_seats, ttl_pax)
    if ttl_pax > occupied_seats:
        raise NotEnoughSeatsOccupiedError(occupied_seats, ttl_pax)
    operating_weight = aircraft.dow + task.takeoff_fuel
    allowed_weight_for_takeoff = min(
        aircraft.mtow, aircraft.mldw + task.trip_fuel, aircraft.mzfw + task.takeoff_fuel
    )
    allowed_traffic_load = allowed_weight_for_takeoff - operating_weight
    total_traffic_load = (
        calc_pax_weight(
            weights,
            task.num_adults,
            task.num_children,
            task.num_infants,
            task.cabin_baggage,
        )
        + task.cargo
    )
    underload_lmc = allowed_traffic_load - total_traffic_load
    if underload_lmc < 0:
        raise PayloadTooHeavyError(total_traffic_load, allowed_traffic_load)
    zfw = aircraft.dow + total_traffic_load
    tow = zfw + task.takeoff_fuel
    ldw = tow - task.trip_fuel
    pax_influence = calc_pax_influence(
        weights,
        aircraft.a_influence,
        aircraft.b_influence,
        aircraft.c_influence,
        aircraft.d_influence,
        task.pax_a,
        task.pax_b,
        task.pax_c,
        task.pax_d,
    )
    cargo_influence = task.cargo * aircraft.cargo_influence
    takeoff_fuel_influence = get_closest_fuel_index(task.takeoff_fuel)
    landing_fuel_influence = get_closest_fuel_index(task.takeoff_fuel - task.trip_fuel)
    lizfw = aircraft.doi + pax_influence + cargo_influence
    litow = lizfw + takeoff_fuel_influence
    lilaw = lizfw + landing_fuel_influence
    maczfw = calc_macrc(lizfw, zfw)
    mactow = calc_macrc(litow, tow)
    maclaw = calc_macrc(lilaw, ldw)
    stab_trim = calc_stab(mactow)
    return CalculationResult(
        aircraft,
        task,
        weights,
        operating_weight,
        allowed_weight_for_takeoff,
        allowed_traffic_load,
        underload_lmc,
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
