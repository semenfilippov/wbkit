import numpy as np
import pytest
from wbkit.interpolables import Interpolable


class TestInterpolable:
    i_obj = Interpolable([(2, 20), (3, 30), (-1, 10)])

    def test_init(self):
        assert np.array_equal(self.i_obj.__xp__, [-1, 2, 3])
        assert np.array_equal(self.i_obj.__fp__, [10, 20, 30])

    @staticmethod
    def test_one_point_raises():
        with pytest.raises(ValueError):
            Interpolable([(1, 10)])

    @staticmethod
    def test_duplicate_values_raise():
        with pytest.raises(ValueError):
            Interpolable([(1, 10), (1, 20)])

    @staticmethod
    @pytest.mark.parametrize(
        ["points"], [([("a", 2), (10, 20)],), ([(1, 2), ("a", 20)],)]
    )
    def test_mistype_raises(points):
        with pytest.raises(TypeError):
            Interpolable(points)

    def test_min_prop(self):
        assert self.i_obj.min_x == -1

    def test_max_prop(self):
        assert self.i_obj.max_x == 3

    def test_validate_in_range_raises_lt(self):
        with pytest.raises(
            ValueError, match=f"x is out of range, should be >= {self.i_obj.min_x}"
        ):
            self.i_obj.__validate_in_range__(-2)

    def test_validate_in_range_raises_gt(self):
        with pytest.raises(
            ValueError, match=f"x is out of range, should be <= {self.i_obj.max_x}"
        ):
            self.i_obj.__validate_in_range__(4)

    @pytest.mark.parametrize(
        ["x", "exp_value"], [(-2, -1), (4, 3), (2.5, 3), (2.4, 2), (2.6, 3)]
    )
    def test_get_nearest_xp(self, x, exp_value):
        assert self.i_obj.__get_nearest_x__(x) == exp_value

    @pytest.mark.parametrize(
        ["x", "exp_value"],
        [*tuple(zip([x / 10 for x in range(20, 31)], range(20, 31)))],
    )
    def test_interpolate(self, x, exp_value):
        assert self.i_obj.interp(x) == exp_value

    @pytest.mark.parametrize(
        ["x", "exp_value"],
        [
            *tuple(zip([x / 10 for x in range(20, 25)], [20] * 5)),
            *tuple(zip([x / 10 for x in range(25, 31)], [30] * 5)),
        ],
    )
    def test_defined_value(self, x, exp_value):
        assert self.i_obj.get_defined_value(x) == exp_value
