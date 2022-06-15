from typing import NamedTuple
from wbkit.plfunc import PLFunction


class CG(NamedTuple):
    value: float
    weight: float


class CGLimits:
    def __init__(self, fwd_line: PLFunction, aft_line: PLFunction):
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
        self.min_weight = fwd_line.min_x
        self.max_weight = fwd_line.max_x

    def in_weight_range(self, weight: float) -> bool:
        return weight in self.fwd

    def exceeds_fwd(self, cg: CG) -> bool:
        return cg.value < self.fwd[cg.weight]

    def exceeds_aft(self, cg: CG) -> bool:
        return cg.value > self.aft[cg.weight]

    def __contains__(self, cg: CG) -> bool:
        return self.in_weight_range(cg.weight) and not (
            self.exceeds_fwd(cg) or self.exceeds_aft(cg)
        )
