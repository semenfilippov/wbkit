class CalculationError(Exception):
    pass


class IncorrectTripFuelError(CalculationError):
    def __init__(self, takeoff_fuel, trip_fuel) -> None:
        super().__init__(
            f"Trip fuel ({takeoff_fuel}) must not exceed "
            f"takeoff fuel ({trip_fuel})."
        )


class OccupiedSeatsMismatchError(CalculationError):
    pass


class TooManySeatsOccupiedError(OccupiedSeatsMismatchError):
    def __init__(self, occupied_seats: int, ttl_pax: int) -> None:
        super().__init__(
            f"Too many seats occupied. The number of occupied seats "
            f"must not exceed total number of PAX. "
            f"Difference: {occupied_seats - ttl_pax}."
        )


class NotEnoughSeatsOccupiedError(OccupiedSeatsMismatchError):
    def __init__(self, occupied_seats: int, ttl_pax: int) -> None:
        super().__init__(
            f"Not enough seats occupied. The number of occupied seats "
            f"must be equal to total number of PAX. "
            f"Difference: {ttl_pax - occupied_seats}."
        )


class PayloadTooHeavyError(CalculationError):
    def __init__(self, total_traffic_load, allowed_traffic_load) -> None:
        super().__init__(
            f"Total traffic load exceeds allowed "
            f"traffic load by {total_traffic_load - allowed_traffic_load} kg."
        )
