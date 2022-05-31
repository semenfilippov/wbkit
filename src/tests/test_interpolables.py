import pytest
from wbkit.interpolables import Interpolable


@pytest.fixture
def ip() -> Interpolable:
    return Interpolable(((2, 20), (3, 30), (-1, 10)))


@pytest.fixture(params=range(20, 31))
def x(request):
    return request.param / 10


@pytest.fixture
def x_exp_interp(x):
    return x * 10


@pytest.fixture
def x_exp_def(x):
    # this looks ugly, but this is the simplest way
    # to avoid round(2.5) returning 2
    return 30 if x == 2.5 else round(x) * 10


def test_init(ip: Interpolable):
    assert ip.__xp__ == (-1, 2, 3)
    assert ip.__fp__ == (10, 20, 30)


def test_duplicate_values_raise():
    with pytest.raises(ValueError, match="duplicate x values are not allowed"):
        Interpolable([(1, 10), (1, 20)])


@pytest.mark.parametrize(["points"], [([("a", 2), (10, 20)],), ([(1, 2), ("a", 20)],)])
def test_mistype_raises(points):
    with pytest.raises(TypeError):
        Interpolable(points)


def test_min_x_prop(ip: Interpolable):
    assert ip.min_x == -1


def test_max_x_prop(ip: Interpolable):
    assert ip.max_x == 3


def test_min_y_prop(ip: Interpolable):
    assert ip.min_y == 10


def test_max_y_prop(ip: Interpolable):
    assert ip.max_y == 30


def test_lt_not_in_range(ip):
    assert -2 not in ip


def test_gt_not_in_range(ip):
    assert 4 not in ip


def test_interpolate(ip, x, x_exp_interp):
    assert ip[x] == x_exp_interp


def test_get_defined(ip, x, x_exp_def):
    assert ip.get_defined_f(x) == x_exp_def
