from __future__ import annotations

from functools import cached_property
from itertools import pairwise
from typing import Sequence, overload

import numpy as np


class PLFunction:
    """Representation of piecewise linear function."""

    def __init__(
        self,
        points: Sequence[tuple[float, float]],
    ) -> None:
        """Create PLFunction object.

        Args:
            points (Sequence[tuple[float, float]]): sequence of (x, f(x)) tuples

        Raises:
            ValueError: if points contain duplicate values for x
        """
        if len(points) == 0:
            raise ValueError("at least one point is required")
        if len({x[0] for x in points}) < len(points):
            raise ValueError("duplicate x values are not allowed")
        self.points = tuple(sorted(points, key=lambda x: x[0]))

    def __cut(
        self, lower: float | None = None, upper: float | None = None
    ) -> PLFunction:
        """Get new PLFunction object with x range cut to given bounds.

        Args:
            lower (float | None, optional): Lower bound. If not set
            or less than self.min_x, defaults to self.min_x
            upper (float | None, optional): Upper bound. If not set
            or greater than self.max_x, defaults to self.max_x

        Raises:
            ValueError: if cutting range bounds are equal or in reverse order

        Returns:
            PLFunction: new PLFunction with x range cut to given bounds
        """
        _lower = max(lower if lower is not None else self.min_x, self.min_x)
        _upper = min(upper if upper is not None else self.max_x, self.max_x)

        if _lower > _upper:
            raise ValueError(f"incorrect cutting range {_lower} - {_upper}")

        points = [x for x in self.points if _lower <= x[0] <= _upper]

        if _lower not in self.xp:
            f_lower = self[_lower]
            lower_tuple = _lower, f_lower
            points.append(lower_tuple)

        if _upper not in self.xp:
            f_upper = self[_upper]
            upper_tuple = _upper, f_upper
            points.append(upper_tuple)

        return PLFunction(points)

    @cached_property
    def xp(self) -> tuple[float, ...]:
        """Tuple of x points.

        Returns:
            tuple[float, ...]: all x points
        """
        return tuple(x[0] for x in self.points)

    @cached_property
    def fp(self) -> tuple[float, ...]:
        """Tuple of f(x) points.

        Returns:
            tuple[float, ...]: all f(x) points
        """
        return tuple(x[1] for x in self.points)

    @property
    def min_x(self) -> float:
        """Minimum x value.

        Returns:
            float: minimum x
        """
        return self.xp[0]

    @property
    def max_x(self) -> float:
        """Maximum x value.

        Returns:
            float: maximum x
        """
        return self.xp[-1]

    @cached_property
    def min_f(self) -> float:
        """Minimum f(x) value.

        Returns:
            float: minimum f(x)
        """
        return min(self.fp)

    @cached_property
    def max_f(self) -> float:
        """Maximum f(x) value.

        Returns:
            float: maximum f(x)
        """
        return max(self.fp)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.points})"

    def __contains__(self, x: float) -> bool:
        return self.min_x <= x <= self.max_x

    @overload
    def __getitem__(self, idx: float) -> float:
        ...

    @overload
    def __getitem__(self, idx: slice) -> PLFunction:
        ...

    def __getitem__(self, idx: float | slice) -> float | PLFunction:
        """
        If `idx` is a single number – get interpolated f(x).
        If `idx` is a slice – get a new PLFunction object
        with x bounds [lower:upper]. Step is meaningless in this
        case and will be ignored if present.

        Args:
            idx (float | slice): number or slice object

        Raises:
            KeyError: if idx is a number outside of x range

        Returns:
            float | PLFunction: interpolated f(x) or PLFunction slice
        """
        if isinstance(idx, slice):
            return self.__cut(idx.start, idx.stop)
        if idx not in self:
            raise KeyError(f"x should be in range {self.min_x} - {self.max_x}")
        if idx in self.xp:
            return self.fp[self.xp.index(idx)]
        return float(np.interp(idx, self.xp, self.fp))

    def defined_f(self, x: float) -> float:
        """Get f(x) for defined x closest to given x value.

        Args:
            x (float): x value to search for

        Raises:
            ValueError: if x is out of defined range

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
            diff1 = y1s - y1o
            diff2 = y2s - y2o
            if diff1 == 0 or diff2 == 0 or diff1 * diff2 < 0:
                return True
        return False
