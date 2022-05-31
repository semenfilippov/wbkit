from shapely.geometry import LineString, Point, Polygon
from shapely.geometry.base import BaseGeometry


class WBGeometry:
    def __init__(self, bg: BaseGeometry) -> None:
        if not isinstance(bg, BaseGeometry):
            raise TypeError("")
        self.__bg__ = bg

    @property
    def bounds(self):
        return self.__bg__.bounds

    @property
    def coords(self):
        return self.__bg__.coords

    @property
    def xy(self):
        return self.__bg__.xy

    @property
    def min_x(self) -> float:
        return self.bounds[0]

    @property
    def max_x(self) -> float:
        return self.bounds[2]

    @property
    def min_y(self) -> float:
        return self.bounds[1]

    @property
    def max_y(self) -> float:
        return self.bounds[3]

    def covers(self, other):
        if isinstance(other, BaseGeometry):
            return self.__bg__.covers(other)
        elif isinstance(other, WBGeometry):
            return self.__bg__.covers(other.__bg__)
        else:
            raise TypeError("")

    def intersection(self, other):
        if isinstance(other, BaseGeometry):
            return self.__bg__.intersection(other)
        elif isinstance(other, WBGeometry):
            return self.__bg__.intersection(other.__bg__)
        else:
            raise TypeError("")

    def intersects(self, other):
        if isinstance(other, BaseGeometry):
            return self.__bg__.intersects(other)
        elif isinstance(other, WBGeometry):
            return self.__bg__.intersects(other.__bg__)
        else:
            raise TypeError("")


class WBPoint(WBGeometry):
    def __init__(self, pt: Point) -> None:
        if not isinstance(pt, Point):
            raise TypeError("")
        super().__init__(pt)

    @property
    def x(self):
        if not isinstance(self.__bg__, Point):
            raise TypeError("")
        return self.__bg__.x

    @property
    def y(self):
        if not isinstance(self.__bg__, Point):
            raise TypeError("")
        return self.__bg__.y


class WBLineString(WBGeometry):
    def __init__(self, ls: LineString) -> None:
        if not isinstance(ls, LineString):
            raise TypeError("")
        super().__init__(ls)


class WBPolygon(WBGeometry):
    def __init__(self, pg: Polygon) -> None:
        if not isinstance(pg, Polygon):
            raise TypeError("")
        super().__init__(pg)
