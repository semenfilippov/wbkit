from typing import Sequence, Tuple, Union

import numpy as np
from shapely.geometry import LineString


class Interpolable:
    def __init__(
        self, points: Sequence[Tuple[Union[int, float], Union[int, float]]]
    ) -> None:
        """Create Interpolable object.

        Args:
            points (Sequence[Tuple[int | float, int | float]]):
                x : f(x) pairs

        Raises:
            ValueError: if len(points) < 2
            ValueError: if points contain duplicate values for x
        """
        if len(points) < 2:
            raise ValueError(
                "You should provide at least two points "
                "to construct Interpolable object"
            )
        if not len(points) == len({x[0] for x in points}):
            raise ValueError("xp values should be unique")
        self.__points__ = tuple(sorted(points, key=lambda x: x[0]))
        self.__xp__ = np.array(tuple(x[0] for x in self.__points__), dtype=np.double)
        self.__fp__ = np.array(tuple(x[1] for x in self.__points__), dtype=np.double)

    @property
    def min_x(self) -> Union[int, float]:
        """Get minumum x value of defined x range.

        Returns:
            int: min(x)
        """
        return np.min(self.__xp__)

    @property
    def max_x(self) -> Union[int, float]:
        """Get maximum x value of defined x range.

        Returns:
            int: max(x)
        """
        return np.max(self.__xp__)

    @property
    def linestring(self) -> LineString:
        return LineString(self.__points__)

    def __validate_in_range__(self, x: Union[int, float]):
        """This method is intended for internal use to validate if
        given x is in defined x range.

        Args:
            x : x value to validate

        Raises:
            `ValueError`: if x is not within Interpolateble object x range
        """
        if x < self.min_x:
            raise ValueError(f"x is out of range, should be >= {self.min_x}")
        if x > self.max_x:
            raise ValueError(f"x is out of range, should be <= {self.max_x}")

    def __get_nearest_x__(self, x: Union[int, float]) -> Union[int, float]:
        """Get defined x value closest to given x.
        If x value is equally distant between two defined values, return greater one.

        Args:
            x (Union[int, float]): requested x value

        Returns:
            Union[int, float]: x value closest to given one
        """
        pos = np.searchsorted(self.__xp__, x)
        if pos == 0:
            return self.__xp__[0]
        if pos == len(self.__xp__):
            return self.__xp__[-1]
        before = self.__xp__[pos - 1]
        after = self.__xp__[pos]
        return after if x - before >= after - x else before

    def intersects(self, other) -> bool:
        """Check if Interpolable function lines intersect.

        Args:
            other (Interpolable): Interpolable object to check intersection with.

        Raises:
            NotImplementedError: if `other` type is not Interpolable

        Returns:
            bool: True if Interpolable objects intersect, otherwise False
        """
        if isinstance(other, Interpolable):
            return self.linestring.intersects(other.linestring)
        raise NotImplementedError(
            f"can only check intersection to other "
            f"Interpolable object, {type(other)} given"
        )

    def interp(self, x: Union[float, int]) -> float:
        """Get interpolated f(x).

        Args:
            x (Union[float, int]): x value to interpolate

        Returns:
            float: interpolated f(x)
        """
        self.__validate_in_range__(x)
        return float(np.interp(x, self.__xp__, self.__fp__))

    def get_defined_value(self, x: Union[float, int]) -> float:
        self.__validate_in_range__(x)
        return self.interp(self.__get_nearest_x__(x))
