from typing import Dict, Union
import numpy as np

LinearFuncPoints = Dict[int, Union[float, int]]


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


class Stab(Interpolable):
    """Stabilizer trim calculator"""

    def __init__(self, points: LinearFuncPoints) -> None:
        """Get new stabilizer trim calculator.

        Args:
            points (Dict[int, Union[int, float]]): stab trim function points,
            where keys are MAC/RC values, values are corresponding stab trim settings
        """
        super().__init__(points)

    def calc(self, mactow: float) -> float:
        """Get takeoff stab trim setting for given %MAC.

        Args:
            mactow (float): %MAC/RC for TOW

        Returns:
            float: stab trim setting
        """
        return self.get_interpolated_value(mactow)


class FuelEffect(Interpolable):
    def __init__(self, points: LinearFuncPoints) -> None:
        """Get new FuelEffect object.

        Args:
            points (Dict[int, Union[int, float]]): fuel effect index influence points,
            where key is fuel quantity, value is index influence
        """
        super().__init__(points)

    def get_influence(self, fuel: int, allow_interpolation: bool = False) -> float:
        """Get index influence for given fuel quantity.

        Args:
            `fuel` (int): fuel quantity
            `allow_interpolation` (bool, optional): Whether to interpolate
            index influence or not.
            Defaults to False.

        Returns:
            `float`: index influence
        """
        if allow_interpolation:
            return self.get_interpolated_value(fuel)
        return self.get_defined_value(fuel)
