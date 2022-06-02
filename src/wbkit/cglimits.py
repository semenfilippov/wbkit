from shapely.geometry import Polygon

from wbkit.geometry import WBPoint, WBPolygon
from wbkit.interpolables import Interpolable


class CG(WBPoint):
    pass


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
        fwd_points = fwd_line.coords
        aft_points = reversed(aft_line.coords)
        super().__init__(Polygon((*fwd_points, *aft_points)))

    def __contains__(self, idx: CG) -> bool:
        return self.covers(idx)
