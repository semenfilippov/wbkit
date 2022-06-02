from bisect import bisect_left
from typing import Optional, Sequence, Tuple

from shapely.geometry import LineString, Point

from wbkit.geometry import WBLineString


class Interpolable(WBLineString):
    def __init__(self, points: Sequence[Tuple[float, float]]) -> None:
        """Create Interpolable object.

        Args:
            points (Sequence[Tuple[int | float, int | float]]):
                x : f(x) pairs

        Raises:
            ValueError: if len(points) < 2
            ValueError: if points contain duplicate values for x
        """
        if not len(points) == len({x[0] for x in points}):
            raise ValueError("duplicate x values are not allowed")
        super().__init__(LineString(sorted(points, key=lambda x: x[0])))

    @property
    def __xp__(self):
        return tuple(self.xy[0])

    @property
    def __fp__(self):
        return tuple(self.xy[1])

    def __contains__(self, x: float) -> bool:
        return self.min_x <= x <= self.max_x

    def get_defined_f(self, x: float) -> Optional[float]:
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

    def __getitem__(self, x: float) -> float:
        """Get f(x).

        Args:
            x (Union[float, int]): x value to interpolate

        Returns:
            float: interpolated f(x)
        """
        if x not in self:
            raise KeyError(f"x should be in range {self.min_x} - {self.max_x}")
        xline = LineString([(x, self.min_y), (x, self.max_y)])
        point = self.intersection(xline)
        if not isinstance(point, Point):
            raise KeyError("unable to get f(x) due internal error")
        return point.y
