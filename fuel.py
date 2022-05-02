FUEL_INDEXES = {
    200: -0.83,
    400: -1.56,
    600: -2.22,
    800: -2.83,
    1000: -3.40,
    1200: -3.92,
    1400: -4.39,
    1600: -4.81,
    1800: -5.17,
    2000: -5.47,
    2200: -5.73,
    2400: -5.93,
    2600: -6.07,
    2800: -6.21,
    3000: -6.32,
    3200: -6.31,
    3400: -6.27,
    3600: -6.27,
    3800: -6.11,
    4000: -6.02,
    4200: -5.60,
    4255: -5.47,
    4400: -6.30,
    4600: -7.38,
    4800: -8.40,
    5000: -9.44,
    5200: -10.56,
    5400: -11.56,
    5600: -12.63,
    5800: -13.69,
    6000: -14.82,
    6200: -15.98,
    6400: -17.28,
    6488: -17.91,
}
MAX_FUEL = max(FUEL_INDEXES)


def get_closest_fuel_index(fuel: int) -> float:
    """Get closest fuel index.

    Args:
        fuel (int): fuel quantity

    Raises:
        ValueError: if fuel value is negative
        ValueError: if fuel value exceeds maximum

    Returns:
        float: index influence
    """
    if fuel < 0:
        raise ValueError(f"Incorrect fuel value: {fuel} (must not be negative).")
    if fuel in FUEL_INDEXES:
        return FUEL_INDEXES[fuel]
    if fuel > MAX_FUEL:
        raise ValueError(f"Incorrect fuel value: {fuel} (must not exceed {MAX_FUEL}).")
    closest_keys = {abs(fuel - x) for x in FUEL_INDEXES}
    min_diff = min(closest_keys)
    if fuel + min_diff in FUEL_INDEXES and fuel - min_diff in FUEL_INDEXES:
        more_fuel_index = FUEL_INDEXES[fuel + min_diff]
        less_fuel_index = FUEL_INDEXES[fuel - min_diff]
        return (
            more_fuel_index
            if abs(more_fuel_index) >= abs(less_fuel_index)
            else less_fuel_index
        )
    if fuel + min_diff in FUEL_INDEXES:
        return FUEL_INDEXES[fuel + min_diff]
    else:
        return FUEL_INDEXES[fuel - min_diff]


class TripInfo:
    def __init__(self, takeoff_fuel, trip_fuel) -> None:
        if takeoff_fuel < 0:
            raise ValueError(
                f"Incorrect take off fuel value: {takeoff_fuel} (must not be negative)."
            )
        if trip_fuel < 0:
            raise ValueError(
                f"Incorrect trip fuel value: {trip_fuel} (must not be negative)."
            )
        if trip_fuel > takeoff_fuel:
            raise ValueError(
                f"Trip fuel ({trip_fuel}) cannot exceed take off fuel ({takeoff_fuel})."
            )
        self.takeoff_fuel = takeoff_fuel
        self.trip_fuel = trip_fuel
        self.takeoff_fuel_index = get_closest_fuel_index(takeoff_fuel)
        self.landing_fuel_index = get_closest_fuel_index(takeoff_fuel - trip_fuel)
