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
        ValueError: if fuel quantity is negative
        ValueError: if fuel quantity exceeds maximum

    Returns:
        float: index influence
    """
    if fuel < 0:
        raise ValueError(f"Incorrect fuel quantity: {fuel} (must not be negative).")
    if fuel in FUEL_INDEXES:
        return FUEL_INDEXES[fuel]
    if fuel > MAX_FUEL:
        raise ValueError(
            f"Incorrect fuel quantity: {fuel} (must not exceed {MAX_FUEL})."
        )
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
