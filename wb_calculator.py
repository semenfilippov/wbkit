"""
A weight and balance calculation module.
"""


from dataclasses import dataclass

# Index formula constants.
# Reference station/axis. Selected station around which all index values are calculated.

REF_STATION = 13.2  # meters from zero
# Constant used as a plus value to avoid negative index figures.
K_CONSTANT = 50
# Constant used as a denominator to convert moment values into index values.
C_CONSTANT = 280

# MAC/RC constants.
# Length of Mean Aerodynamic Chord / Reference Chord in length units.
MACRC_LENGTH = 2.526  # meters
# Horizontal distance in length units from the station zero
# to location of the Leading Edge of the MAC / RC
LEMAC_AT = 12.542  # meters from zero


def calc_index(weight: float, station: float) -> float:
    """Calculate index.

    Args:
        weight (float): actual weight
        station (float): horizontal distance in meters
        from station zero to the location

    Returns:
        float: index
    """
    return float((weight * (station - REF_STATION)) / C_CONSTANT + K_CONSTANT)


def calc_macrc(idx: float, weight: float) -> float:
    """Calculate MAC/RC.

    Args:
        idx (float): index value corresponding to respective weight
        weight (float): actual weight

    Returns:
        float: MAC/RC
    """
    return (((C_CONSTANT * (idx - K_CONSTANT)) / weight) + REF_STATION - LEMAC_AT) / (
        MACRC_LENGTH / 100
    )


@dataclass
class AircraftConfig:
    dow: int  # dry operating weight
    doi: float  # dry operating index
    area_a_capacity: int  # number of pax
    area_b_capacity: int  # number of pax
    area_c_capacity: int  # number of pax
    area_d_capacity: int  # number of pax
    area_a_index_influence: int  # per 1 kg
    area_b_index_influence: int  # per 1 kg
    area_c_index_influence: int  # per 1 kg
    area_d_index_influence: int  # per 1 kg
    cargo_comp_index_effect: int  # per 1 kg
