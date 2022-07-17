from __future__ import annotations

from typing import NamedTuple, Sequence

from wbkit.plfunc import PLFunction


class CG(NamedTuple):
    value: float
    weight: float
    limits: CGLimits | None = None

    @property
    def __limits(self) -> CGLimits:
        """Unwrap obj.limits optional

        Raises:
            TypeError: if obj.limits is None

        Returns:
            CGLimits: CGLimits object
        """
        if self.limits is None:
            raise TypeError("CG object has no assigned limits")
        return self.limits

    @property
    def in_limits(self) -> bool:
        """Shorthand for obj in obj.limits"""
        return self in self.__limits

    @property
    def limit_range(self) -> tuple[float, float] | None:
        """Shorthand for obj.limits.limit_range(self.weight)"""
        return self.__limits.limit_range(self.weight)

    @property
    def exceeds_fwd(self) -> bool:
        """Shorthand for obj.limits.cg_exceeds_aft(self)"""
        return self.__limits.cg_exceeds_fwd(self)

    @property
    def exceeds_aft(self) -> bool:
        """Shorthand for obj.limits.cg_exceeds_aft(self)"""
        return self.__limits.cg_exceeds_aft(self)


class CGLimits:
    def __init__(
        self,
        fwd: Sequence[tuple[float, float]] | PLFunction,
        aft: Sequence[tuple[float, float]] | PLFunction,
    ):
        """Create new CGLimits object.

        Args:
            fwd (Sequence[tuple[float, float]] | PLFunction): forward CG limit line
            aft (Sequence[tuple[float, float]] | PLFunction): aft CG limit line

        Raises:
            ValueError: if forward and aft lines have different min and max x
            ValueError: if lines overlap
            ValueError: if lines are passed in wrong order
        """
        _fwd = fwd if isinstance(fwd, PLFunction) else PLFunction(fwd)
        _aft = aft if isinstance(aft, PLFunction) else PLFunction(aft)
        if not (_fwd.min_x == _aft.min_x and _fwd.max_x == _aft.max_x):
            raise ValueError(
                "fwd_line and aft_line min and max weights should be equal"
            )
        if _fwd.intersects(_aft):
            raise ValueError("fwd_line and aft_line should not overlap")
        if _fwd.min_f > _aft.min_f and _fwd.max_f > _aft.max_f:
            raise ValueError("make sure order of lines is fwd, aft")
        self.fwd = _fwd
        self.aft = _aft

    @property
    def min_weight(self) -> float:
        """Minimum weight.

        Returns:
            float: minimum weight
        """
        return self.fwd.min_x

    @property
    def max_weight(self) -> float:
        """Maximum weight.

        Returns:
            float: maximum weight
        """
        return self.fwd.max_x

    def cut_weight_range(
        self, min: float | None = None, max: float | None = None
    ) -> CGLimits:
        """Return new CGLimits object with weight range cut to min and max
        values accordingly. This functionality relies on PLFunction.cut()
        method.

        Args:
            min (float | None, optional): minimum weight. Defaults to None.
            max (float | None, optional): maximum weight. Defaults to None.

        Returns:
            CGLimits: CGLimits object
        """
        new_fwd = self.fwd.cut(min, max)
        new_aft = self.aft.cut(min, max)
        return CGLimits(new_fwd, new_aft)

    def limit_range(self, for_weight: float) -> tuple[float, float] | None:
        """Get tuple containing forward and aft CG limits for given weight.
        If weight is outside of defined weight range – None is returned.

        Args:
            for_weight (float): weight

        Returns:
            tuple[float, float] | None: fwd, aft limits tuple or None
        """
        try:
            fwd, aft = self.fwd[for_weight], self.aft[for_weight]
        except KeyError:
            return None
        return fwd, aft

    def __contains__(self, cg: CG) -> bool:
        """Check if CG object is in limits. CG object with weight outside of defined
        weight range is considered to be out of limits.

        Args:
            cg (CG): CG object

        Returns:
            bool: True if CG object is in limits, False otherwise
        """
        limits = self.limit_range(cg.weight)
        if limits is None:
            return False
        fwd, aft = limits
        return not (cg.value < fwd or cg.value > aft)

    def exceeds_fwd(self, value: float, weight: float) -> bool:
        """Check if value-weight pair exceed forward CG limits.
        True is always returned if weight is out of defined weight range.

        Args:
            value (float): cg value
            weight (float): cg weight

        Returns:
            bool | None: False if value-weight pair does not exceed forward limits,
            True if does.
        """
        limits = self.limit_range(weight)
        if limits is None:
            return True
        fwd, _ = limits
        return value < fwd

    def exceeds_aft(self, value: float, weight: float) -> bool:
        """Check if value-weight pair exceed aft CG limits.
        True is always returned if weight is out of defined weight range.

        Args:
            value (float): cg value
            weight (float): cg weight

        Returns:
            bool | None: False if value-weight pair does not exceed aft limits,
            True if does.
        """
        limits = self.limit_range(weight)
        if limits is None:
            return True
        _, aft = limits
        return value > aft

    def cg_exceeds_fwd(self, cg: CG) -> bool:
        """Check if CG object exceeds forward CG limits.
        True is always returned if weight is out of defined weight range.

        Args:
            cg (CG): cg object

        Returns:
            bool | None: False if CG object does not exceed forward limits,
            True if does. None if weight is out of range.
        """
        return self.exceeds_fwd(cg.value, cg.weight)

    def cg_exceeds_aft(self, cg: CG) -> bool:
        """Check if CG object exceeds aft CG limits.
        True is always returned if weight is out of defined weight range.

        Args:
            cg (CG): cg object

        Returns:
            bool | None: False if CG object does not exceed aft limits,
            True if does. None if weight is out of range.
        """
        return self.exceeds_aft(cg.value, cg.weight)
