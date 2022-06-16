from __future__ import annotations

from functools import cached_property
from itertools import pairwise
from typing import Sequence

import numpy as np


class PLFunction:
    """Representation of piecewise linear function."""

    def __init__(self, points: Sequence[tuple[float, float]]) -> None:
        """Create PLFunction object.

        Args:
            points (Sequence[tuple[float, float]]): sequence of (x, f(x)) tuples

        Raises:
            ValueError: if points contain duplicate values for x
        """
        if len({x[0] for x in points}) < len(points):
            raise ValueError("duplicate x values are not allowed")
        self.points = tuple(sorted(points, key=lambda x: x[0]))

    @cached_property
    def xp(self) -> tuple[float, ...]:
        return tuple(x[0] for x in self.points)

    @cached_property
    def fp(self) -> tuple[float, ...]:
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

    def __getitem__(self, x: float) -> float | None:
        """Get f(x).

        Args:
            x (float): x value to interpolate

        Returns:
            float | None: interpolated f(x) if x is within defined range, otherwise None
        """
        if x not in self:
            return None
        if x in self.xp:
            return self.fp[self.xp.index(x)]
        return float(np.interp(x, self.xp, self.fp))

    def defined_f(self, x: float) -> float | None:
        """Get f(x) for defined x closest to given x value.

        Args:
            x (float): x value to search for

        Returns:
            float | None: f( closest defined x )
            if x is within defined range, otherwise None
        """
        if x not in self:
            return None
        pos = np.searchsorted(self.xp, x)
        if pos == 0:
            return self.fp[0]
        if pos == len(self.xp):
            return self.fp[-1]
        before = self.xp[pos - 1]
        after = self.xp[pos]
        return self.fp[pos] if x - before >= after - x else self.fp[pos - 1]

    def overlaps_with(self, other: PLFunction) -> bool:
        """Check if two piecewise linear function graphs overlap.

        Args:
            other (PLFunction): other PLFunction

        Returns:
            bool: True if PLFunction graphs overlap, False otherwise
        """
        if self.min_x > other.max_x or self.max_x < other.min_x:
            return False
        all_xp = self.xp + other.xp
        common_xp = set(filter(lambda x: x in self and x in other, all_xp))
        sorted_xp = sorted(common_xp)
        for x1, x2 in pairwise(sorted_xp):
            y1s, y1o = self[x1], other[x1]
            y2s, y2o = self[x2], other[x2]
            assert (
                y1s is not None
                and y1o is not None
                and y2s is not None
                and y2o is not None
            )
            diff1 = y1s - y1o
            diff2 = y2s - y2o
            if diff1 == 0 or diff2 == 0 or diff1 * diff2 < 0:
                return True
        return False
