import pytest
from wbkit.interpolables import Interpolable


@pytest.fixture
def interpolable() -> Interpolable:
    return Interpolable(((2, 20), (3, 30), (-1, 10)))


@pytest.fixture
def x():
    pass


class TestInterpolable:
    def test_init(self, interpolable: Interpolable):
        assert interpolable.__xp__ == (-1, 2, 3)
        assert interpolable.__fp__ == (10, 20, 30)

    def test_duplicate_values_raise(self):
        with pytest.raises(ValueError, match="duplicate x values are not allowed"):
            Interpolable([(1, 10), (1, 20)])

    @staticmethod
    @pytest.mark.parametrize(
        ["points"], [([("a", 2), (10, 20)],), ([(1, 2), ("a", 20)],)]
    )
    def test_mistype_raises(points):
        with pytest.raises(TypeError):
            Interpolable(points)

    def test_min_x_prop(self, interpolable: Interpolable):
        assert interpolable.min_x == -1

    def test_max_x_prop(self, interpolable: Interpolable):
        assert interpolable.max_x == 3

    def test_min_y_prop(self, interpolable: Interpolable):
        assert interpolable.min_y == 10

    def test_max_y_prop(self, interpolable: Interpolable):
        assert interpolable.max_y == 30

    def test_lt_not_in_range(self, interpolable):
        assert -2 not in interpolable

    def test_gt_not_in_range(self, interpolable):
        assert 4 not in interpolable

    def test_interpolate(self, interpolable: Interpolable, x):
        pass  # TODO: IMPLEMENT THIS!

    def test_get_defined():
        pass  # TODO: IMPLEMENT THIS!
