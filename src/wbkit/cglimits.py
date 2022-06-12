from typing import NamedTuple

from wbkit.interpolable import Interpolable


class CG(NamedTuple):
    value: float
    weight: float


class CGLimits:
    def __init__(
        self,
        fwd_line: Interpolable,
        aft_line: Interpolable,
    ):
        if not (fwd_line.min_x == aft_line.min_x and fwd_line.max_x == aft_line.max_x):
            raise ValueError(
                "fwd_line and aft_line min and max weights should be equal"
            )
        if fwd_line.intersects(aft_line):
            raise ValueError("fwd_line and aft_line should not intersect")
        if fwd_line.min_f > aft_line.min_f and fwd_line.max_f > aft_line.max_f:
            raise ValueError("make sure order of lines is fwd, aft")
        self.__fwd = fwd_line
        self.__aft = aft_line
        self.min_weight = fwd_line.min_x
        self.max_weight = fwd_line.max_x

    def __contains__(self, cg: CG) -> bool:
        return (
            self.min_weight <= cg.weight <= self.max_weight
            and cg.value >= self.__fwd[cg.weight]
            and cg.value <= self.__aft[cg.weight]
        )
