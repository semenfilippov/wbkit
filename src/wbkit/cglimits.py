from typing import Sequence, Tuple, Union
from wbkit.basic import Index
from wbkit.interpolables import Interpolable


class LimitLine(Interpolable):
    def __init__(
        self,
        points: Sequence[Tuple[Union[int, float], Union[int, float]]],
        ref_st: float,
        k: int,
        c: int,
    ) -> None:
        super().__init__(points)
        self.ref_st = ref_st
        self.k = k
        self.c = c

    @staticmethod
    def from_idx_seq(indices: Sequence[Index]):
        if len(indices) < 2:
            raise ValueError(
                "at least two indices should be provided to create LimitLine"
            )
        rkc = {(x.ref_st, x.k, x.c) for x in indices}
        if len(rkc) > 1:
            raise ValueError(
                "unable to initialize LimitLine from Index sequence "
                "objects having different ref_st, c or k attributes:\n"
                + "\n".join(
                    [f"{n}: REF_ST={x[0]} K={x[1]} C={x[2]}" for n, x in enumerate(rkc)]
                )
            )
        ref_st, k, c = rkc.pop()
        return LimitLine([(x.weight, x.value) for x in indices], ref_st, k, c)

    def get_limit_idx(self, weight: int) -> Index:
        return Index(self.interp(weight), weight, self.ref_st, self.c, self.k)
