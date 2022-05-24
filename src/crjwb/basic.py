from typing import Dict, Union
import numpy as np


LinearFuncPoints = Dict[int, Union[float, int]]


class BasicCalc:
    def __init__(
        self,
        ref_station: float,
        k_constant: int,
        c_constant: int,
        macrc_length: float,
        lemac_at: float,
    ) -> None:
        """Initialize BasicCalc.

        Args:
            `ref_station` (float): Reference station/axis. Selected station \
                around which all index values are calculated.
            `k_constant` (int): Constant used as a plus value to avoid \
                negative index figures.
            `c_constant` (int): Constant used as a denominator to convert \
                moment values into index values.
            `macrc_length` (float): Length of \
                Mean Aerodynamic Chord / Reference Chord in length units.
            `lemac_at` (float): Horizontal distance in length units \
                from the station zero to location of the Leading Edge of the MAC / RC.
        """
        self.ref_station = ref_station
        self.k_constant = k_constant
        self.c_constant = c_constant
        self.macrc_length = macrc_length
        self.lemac_at = lemac_at

    def calc_index(self, weight: float, station: float) -> float:
        """Calculate index.

        Args:
            `weight` (float): actual weight
            `station` (float): horizontal distance in meters
        from station zero to the location

        Returns:
            `float`: index
        """
        return float(
            (weight * (station - self.ref_station)) / self.c_constant + self.k_constant
        )

    def calc_macrc(self, idx: float, weight: float) -> float:
        """Calculate MAC/RC.

        Args:
            `idx` (float): index value corresponding to respective weight
            `weight` (float): actual weight

        Returns:
            `float`: MAC/RC
        """
        return (
            ((self.c_constant * (idx - self.k_constant)) / weight)
            + self.ref_station
            - self.lemac_at
        ) / (self.macrc_length / 100)


class Interpolable:
    def __init__(self, points: LinearFuncPoints) -> None:
        """Create Interpolable object.

        Args:
            `points` LinearFuncPoints: {x: f(x)} dict,
            order of x values may be arbitrary

        Raises:
            `ValueError`: if len(points) < 2
        """
        if len(points) < 2:
            raise ValueError(
                "You should provide at least two points "
                "to construct Interpolateble object!"
            )
        self.__points__ = points
        self.__xp__ = sorted([x for x in self.__points__])
        self.__fp__ = [points[x] for x in self.__xp__]
        self.__min_x__ = min(self.__xp__)
        self.__max_x__ = max(self.__xp__)

    def get_min(self) -> int:
        """Get minumum x value of defined x range.

        Returns:
            `int`: min(x)
        """
        return self.__min_x__

    def get_max(self) -> int:
        """Get maximum x value of defined x range.

        Returns:
            `int`: max(x)
        """
        return self.__max_x__

    def __validate_in_range__(self, x: Union[float, int]):
        """This method is intended for internal use to validate if
        given `x` is in defined x range.

        Args:
            `x` (Union[float, int]): x value to validate

        Raises:
            `ValueError`: if `x` is not within Interpolateble object x range
        """
        if x < self.__min_x__:
            raise ValueError(f"x is out of range, should be >= {self.__min_x__}")
        if x > self.__max_x__:
            raise ValueError(f"x is out of range, should be <= {self.__max_x__}")

    def get_interpolated_value(self, x: Union[float, int]) -> float:
        """Get interpolated f(x).

        Args:
            `x` (Union[float, int]): x value to interpolate

        Returns:
            `float`: interpolated f(x)
        """
        self.__validate_in_range__(x)
        return float(np.interp(x, self.__xp__, self.__fp__))

    def get_defined_value(self, x: int) -> Union[float, int]:
        """Get nearest defined f(x).

        WARNING! In this method `x` is explicitly converted
        to int to avoid unexpected behaviour
        due floating points calculation errors.

        The logic of this method is as follows.

        If `x` is found among `self.points` keys, return its value.

        If not, calculate minimal distance between given x
        and each key in `self.points`. If there is more than one value
        for `self.points[x+-difference]`, return the one which
        has greater absolute value.


        Args:
            `x` (int): x value

        Returns:
            `float | int`: nearest defined f(x)
        """
        if x in self.__points__:
            return self.__points__[x]
        x = int(x)
        self.__validate_in_range__(x)
        min_diff = min({abs(x - f) for f in self.__points__})
        possible_values = [
            self.__points__[xd]
            for xd in {x + min_diff, x - min_diff}
            if xd in self.__points__
        ]
        if len(possible_values) > 1:
            return (
                possible_values[0]
                if abs(possible_values[0]) >= abs(possible_values[1])
                else possible_values[1]
            )
        return possible_values[0]
