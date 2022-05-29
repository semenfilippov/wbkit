from typing import Dict, Hashable, Optional, Sequence, Tuple, Union

from wbkit.basic import Index, IndexConstants
from wbkit.interpolables import Interpolable


class LimitLine(Interpolable):
    """Object representing CG Limit line."""

    def __init__(
        self,
        points: Sequence[Tuple[Union[int, float], Union[int, float]]],
        rck: IndexConstants,
    ) -> None:
        """Create LimitLine object.

        Args:
            points (Sequence[Tuple[int |float, int | float]]]): weight-index pairs
            ref_st (float): Reference station/axis. Selected station
            around which all index values are calculated
            c (int): Constant used as a denominator to convert
            moment values into index values
            k (int): Constant used as a plus value to avoid
            negative index figures
        """
        super().__init__(points)
        self.rck = rck

    @classmethod
    def from_idxs(cls, indices: Sequence[Index]):
        """Initialize LimitLine object using sequence of Index objects.
        All Index objects should have the same ref_st, c and k attributes.

        Args:
            indices (Sequence[Index]): sequence of Index objects

        Raises:
            ValueError: if sequence has less than two Index objects
            ValueError: if Index objects have different ref_st, c and k attributes

        Returns:
            LimitLine: LimitLine object
        """
        if len(indices) < 2:
            raise ValueError(
                "at least two indices should be provided to create LimitLine"
            )
        rck_set = {(x.rck) for x in indices}
        if len(rck_set) > 1:
            raise ValueError(
                "unable to initialize LimitLine from Index sequence "
                "objects having different ref_st, c or k attributes:\n"
                + "\n".join(
                    [
                        f"{n}: REF_ST={x.ref_st} C={x.c} K={x.k}"
                        for n, x in enumerate(rck_set)
                    ]
                )
            )
        rck = rck_set.pop()
        return cls(tuple((x.weight, x.value) for x in indices), rck)

    def get_limit_idx(self, weight: int) -> Index:
        return Index(self.interp(weight), weight, self.rck)


class CGLimits:
    def __init__(
        self,
        rck: Optional[IndexConstants],
        limits: Optional[Sequence[Tuple[Hashable, LimitLine, LimitLine]]] = None,
    ) -> None:
        self.rck = rck
        self.__phases__: Dict[Hashable, Tuple[LimitLine, LimitLine]] = dict()
        if limits:
            for limit in limits:
                self.add_limits(limit[0], limit[1], limit[2])

    def add_limits(self, phase: Hashable, fwd_line: LimitLine, aft_line: LimitLine):
        if not fwd_line.rck == aft_line.rck:
            raise ValueError(
                "both fwd and aft LimitLine objects should have "
                "the same ref_st, k and c attribute values"
            )
        if self.rck is None:
            self.rck = fwd_line.rck
        if len({self.rck, fwd_line.rck}) > 1:
            raise ValueError(
                "CGLimits object cannot have LimitLines with "
                "different IndexConstants"
            )
        if fwd_line.intersects(aft_line):
            raise ValueError("forward and aft limits should not intersect")
        self.__phases__.update({phase: (fwd_line, aft_line)})

    def idx_in_limits(self, phase: Hashable, idx: Index) -> Tuple[bool, bool]:
        if phase not in self.__phases__:
            raise ValueError(f'limits for phase "{phase}" are not defined')
        return not idx < self.__phases__[phase][0].get_limit_idx(
            idx.weight
        ), not idx > self.__phases__[phase][1].get_limit_idx(idx.weight)
