from typing import NamedTuple

from wbkit.plfunc import PLFunction


class CG(NamedTuple):
    value: float
    weight: float


class CGLimits:
    def __init__(self, fwd_line: PLFunction, aft_line: PLFunction):
        """Create new CGLimits object.

        Args:
            fwd_line (PLFunction): forward CG limit line
            aft_line (PLFunction): aft CG limit line

        Raises:
            ValueError: if forward and aft lines have different min and max x
            ValueError: if lines overlap
            ValueError: if lines are passed in wrong order
        """
        if not (fwd_line.min_x == aft_line.min_x and fwd_line.max_x == aft_line.max_x):
            raise ValueError(
                "fwd_line and aft_line min and max weights should be equal"
            )
        if fwd_line.overlaps_with(aft_line):
            raise ValueError("fwd_line and aft_line should not overlap")
        if fwd_line.min_f > aft_line.min_f and fwd_line.max_f > aft_line.max_f:
            raise ValueError("make sure order of lines is fwd, aft")
        self.fwd = fwd_line
        self.aft = aft_line

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

    def get_limits(self, for_weight: float) -> tuple[float, float] | None:
        """Get tuple containing forward and aft CG limits for given weight.
        If weight is outside of range – None is returned.

        Args:
            for_weight (float): weight

        Returns:
            tuple[float, float] | None: fwd, aft limits tuple or None
        """
        fwd, aft = self.fwd[for_weight], self.aft[for_weight]
        if fwd is None or aft is None:
            return None
        return fwd, aft

    def __contains__(self, cg: CG) -> bool:
        """Check if CG object is in limits. CG with weight outside of defined range
        is considered to be out of limits.

        Args:
            cg (CG): CG object

        Returns:
            bool: True if CG object is in limits, False otherwise
        """
        limits = self.get_limits(cg.weight)
        if limits is None:
            return False
        fwd, aft = limits
        return not (cg.value < fwd or cg.value > aft)
