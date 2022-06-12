from __future__ import annotations

from functools import cached_property
from itertools import tee
from typing import Iterable, Sequence, Tuple

import numpy as np


def _pairwise(iterable: Iterable) -> zip:
    """
    >>> _pairwise('ABCDEFG') --> AB BC CD DE EF FG

    Taken from https://docs.python.org/3/library/itertools.html#itertools.pairwise

    Args:
        iterable (Iterable): any iterable

    Returns:
        zip: zip object
    """
    #
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class Interpolable:
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
        self.points = tuple(sorted(points, key=lambda x: x[0]))

    @cached_property
    def xp(self) -> Tuple[float, ...]:
        return tuple(x[0] for x in self.points)

    @cached_property
    def fp(self) -> Tuple[float, ...]:
        return tuple(x[1] for x in self.points)

    @property
    def min_x(self) -> float:
        return self.xp[0]

    @property
    def max_x(self) -> float:
        return self.xp[-1]

    @cached_property
    def min_f(self) -> float:
        return min(self.fp)

    @cached_property
    def max_f(self) -> float:
        return max(self.fp)

    def __contains__(self, x: float) -> bool:
        return self.min_x <= x <= self.max_x

    def __getitem__(self, x: float) -> float:
        """Get f(x).

        Args:
            x (Union[float, int]): x value to interpolate

        Returns:
            float: interpolated f(x)
        """
        if x not in self:
            raise KeyError(f"x should be in range {self.min_x} - {self.max_x}")
        return float(np.interp(x, self.xp, self.fp))

    def defined_f(self, x: float) -> float:
        """Get f(x) for defined x closest to given x value.

        Args:
            x (float): x value to search for

        Raises:
            ValueError: if given x value is out of range

        Returns:
            float: f( closest defined x )
        """
        if x not in self:
            raise ValueError(f"x should be in range {self.min_x} - {self.max_x}")
        pos = np.searchsorted(self.xp, x)
        if pos == 0:
            return self.fp[0]
        if pos == len(self.xp):
            return self.fp[-1]
        before = self.xp[pos - 1]
        after = self.xp[pos]
        return self.fp[pos] if x - before >= after - x else self.fp[pos - 1]

    def intersects(self, other: Interpolable) -> bool:
        """Check if there is an intersection between two interpolable objects.

        Args:
            other (Interpolable): other Interpolable

        Returns:
            bool: True if Interpolables intersect, False otherwise
        """
        if self.min_x > other.max_x or self.max_x < other.min_x:
            return False
        all_xp = self.xp + other.xp
        common_xp = set(filter(lambda x: x in self and x in other, all_xp))
        sorted_xp = sorted(common_xp)
        for x1, x2 in _pairwise(sorted_xp):
            diff1 = self[x1] - other[x1]
            diff2 = self[x2] - other[x2]
            if diff1 == 0 or diff2 == 0 or diff1 * diff2 < 0:
                return True
        return False
