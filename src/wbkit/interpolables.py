from typing import Dict, Sequence, Tuple, Union
import numpy as np


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
        sorted_points = sorted(points, key=lambda x: x[0])
        self.__xp__ = np.array([x[0] for x in sorted_points], dtype=np.double)
        self.__fp__ = np.array([x[1] for x in sorted_points], dtype=np.double)

    @staticmethod
    def from_dict(points: Dict[Union[int, float], Union[int, float]]):
        """Initialize Interpolable object using dict.

        Args:
            points (Dict[int | float, int | float]):
                x : f(x) pairs

        Returns:
            Interpolable: Interpolable object
        """
        return Interpolable([(x, points[x]) for x in points])

    @staticmethod
    def from_lists(xp: Sequence[Union[int, float]], fp: Sequence[Union[int, float]]):
        """Initialize Interpolable object using sequences of xp and fp values.

        Args:
            xp (Sequence[int | float]): x values
            fp (Sequence[int | float]): f(x) values

        Returns:
            Interpolable: Interpolable object
        """
        return Interpolable(list(zip(xp, fp)))

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
