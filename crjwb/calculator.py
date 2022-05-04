from crjwb.cabinareatrim import calc_pax_weight
from crjwb.exceptions import (
    IncorrectTripFuelError,
    NotEnoughSeatsOccupiedError,
    PayloadTooHeavyError,
    TooManySeatsOccupiedError,
)
from crjwb.inputclasses import AircraftData, CalculationTask, StandardWeights


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
    law = tow - task.trip_fuel
