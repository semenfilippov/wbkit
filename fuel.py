__fuel_indexes__ = {
    500: -1.9,
    1000: -3.4,
    1500: -4.6,
    2000: -5.5,
    2500: -6.0,
    3000: -6.3,
    3500: -6.3,
    4000: -6.0,
    4500: -6.8,
    5000: -9.4,
    5500: -12.1,
    6000: -14.8,
    6488: -17.9,
}


def get_closest_fuel_index(fuel: int):
    return __fuel_indexes__[min(__fuel_indexes__.keys(), key=lambda x: abs(x - fuel))]
