from bisect import bisect_left
from typing import Optional, Sequence, Tuple, Union

from shapely.geometry import LineString, Point


class Interpolable(LineString):
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
        super().__init__(sorted(points, key=lambda x: x[0]))
        if not len(self.coords) == len({x[0] for x in self.coords}):
            raise ValueError("duplicate x values are not allowed")

    @property
    def min_x(self) -> Union[int, float]:
        """Get minumum x value of defined x range.

        Returns:
            int: min(xp)
        """
        return self.bounds[0]

    @property
    def max_x(self) -> Union[int, float]:
        """Get maximum x value of defined x range.

        Returns:
            int: max(xp)
        """
        return self.bounds[2]

    @property
    def min_y(self) -> Union[int, float]:
        """Get minumum defined f(x).

        Returns:
            int: min(fp)
        """
        return self.bounds[1]

    @property
    def max_y(self) -> Union[int, float]:
        """Get maximum defined f(x).

        Returns:
            int: max(fp)
        """
        return self.bounds[3]

    @property
    def __xp__(self):
        return tuple(self.xy[0])

    @property
    def __fp__(self):
        return tuple(self.xy[1])

    def __contains__(self, x: Union[int, float]) -> bool:
        return self.min_x <= x <= self.max_x

    def get_defined_f(self, x: Union[int, float]) -> Optional[float]:
        if x not in self:
            raise ValueError(f"x should be in range {self.min_x} - {self.max_x}")
        pos = bisect_left(self.__xp__, x)
        if pos == 0:
            return self.__fp__[0]
        if pos == len(self.__xp__):
            return self.__fp__[-1]
        before = self.__xp__[pos - 1]
        after = self.__xp__[pos]
        return self.__fp__[pos] if x - before >= after - x else self.__fp__[pos - 1]

    def __getitem__(self, x: Union[float, int]) -> float:
        """Get f(x).

        Args:
            x (Union[float, int]): x value to interpolate

        Returns:
            float: interpolated f(x)
        """
        if x not in self:
            raise KeyError(f"key should be in range {self.min_x} - {self.max_x}")
        point = self.intersection(LineString([(x, self.min_y), (x, self.max_y)]))
        if not isinstance(point, Point):
            raise KeyError("unable to get f(x) due internal error")
        return point.y
