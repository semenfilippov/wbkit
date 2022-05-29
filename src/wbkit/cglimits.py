from typing import Sequence, Tuple, Union

from wbkit.basic import Index, PercentMAC
from wbkit.interpolables import Interpolable


class LimitLine(Interpolable):
    """Object representing CG Limit line."""

    def __init__(
        self,
        points: Sequence[Tuple[Union[int, float], Union[int, float]]],
        ref_st: float,
        c: int,
        k: int,
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
        self.ref_st = ref_st
        self.c = c
        self.k = k

    @staticmethod
    def from_idxs(indices: Sequence[Index]):
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
        rck = {(x.ref_st, x.c, x.k) for x in indices}
        if len(rck) > 1:
            raise ValueError(
                "unable to initialize LimitLine from Index sequence "
                "objects having different ref_st, c or k attributes:\n"
                + "\n".join(
                    [f"{n}: REF_ST={x[0]} C={x[1]} K={x[2]}" for n, x in enumerate(rck)]
                )
            )
        ref_st, c, k = rck.pop()
        return LimitLine(tuple((x.weight, x.value) for x in indices), ref_st, c, k)

    @staticmethod
    def from_wght_pctmac_pairs(
        wght_pctmac_pairs: Sequence[Tuple[int, PercentMAC]],
        ref_st: float,
        c: int,
        k: int,
    ):
        """Initialize LimitLine object using sequence of Index objects converted
        from given weight-PercentMAC pairs.

        Args:
            wght_pctmac_pairs (Sequence[Tuple[int, PercentMAC]]): weight-PercentMAC
            pairs
            ref_st (float): Reference station/axis. Selected station
            around which all index values are calculated
            c (int): Constant used as a denominator to convert
            moment values into index values
            k (int): Constant used as a plus value to avoid
            negative index figures

        Returns:
            LimitLine: LimitLine object
        """
        return LimitLine.from_idxs(
            tuple(x[1].to_idx(x[0], ref_st, c, k) for x in wght_pctmac_pairs)
        )

    def get_limit_idx(self, weight: int) -> Index:
        return Index(self.interp(weight), weight, self.ref_st, self.c, self.k)
