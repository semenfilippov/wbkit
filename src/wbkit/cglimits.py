from shapely.geometry import Polygon, Point

from wbkit.geometry import WBPoint, WBPolygon
from wbkit.interpolables import Interpolable


class CG(WBPoint):
    def __init__(self, idx: float, weight: float) -> None:
        self.idx = idx
        self.weight = weight
        super().__init__(Point(weight, idx))


class CGLimits(WBPolygon):
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
        if fwd_line.min_y > aft_line.min_y and fwd_line.max_y > aft_line.max_y:
            raise ValueError("make sure order of lines is fwd, aft")
        self.__fwd = fwd_line
        self.__aft = aft_line
        self.min_weight = fwd_line.min_x
        self.max_weight = fwd_line.max_x
        fwd_points = fwd_line.coords
        aft_points = reversed(aft_line.coords)
        super().__init__(Polygon((*fwd_points, *aft_points)))

    def __contains__(self, cg: CG) -> bool:
        return self.covers(cg)
