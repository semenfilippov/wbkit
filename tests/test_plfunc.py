import pytest
from wbkit.plfunc import PLFunction


@pytest.fixture
def pl() -> PLFunction:
    return PLFunction(((2, 20), (3, 30), (-1, 10)))


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


def test_init(pl: PLFunction):
    assert pl.xp == (-1, 2, 3)
    assert pl.fp == (10, 20, 30)


def test_duplicate_values_raise():
    with pytest.raises(ValueError, match="duplicate x values are not allowed"):
        PLFunction([(1, 10), (1, 20)])


@pytest.mark.parametrize(["points"], [([("a", 2), (10, 20)],), ([(1, 2), ("a", 20)],)])
def test_mistype_raises(points):
    with pytest.raises(TypeError):
        PLFunction(points)


def test_min_x_prop(pl: PLFunction):
    assert pl.min_x == -1


def test_max_x_prop(pl: PLFunction):
    assert pl.max_x == 3


def test_min_f_prop(pl: PLFunction):
    assert pl.min_f == 10


def test_max_f_prop(pl: PLFunction):
    assert pl.max_f == 30


def test_lt_not_in_range(pl):
    assert -2 not in pl


def test_gt_not_in_range(pl):
    assert 4 not in pl


def test_getitem_out_of_range_raises(pl: PLFunction):
    with pytest.raises(KeyError, match=f"x should be in range {pl.min_x} - {pl.max_x}"):
        pl[-2]


def test_getitem(pl, x, x_exp_interp):
    assert pl[x] == x_exp_interp


def test_getslice_wrong_order_raises():
    lower = 1
    upper = 9
    initial = PLFunction([(0, 0), (10, 100)])
    with pytest.raises(ValueError, match=f"incorrect cutting range {upper} - {lower}"):
        initial[upper:lower]


def test_getslice_equal_bounds_raise():
    initial = PLFunction([(0, 0), (10, 100)])
    with pytest.raises(ValueError, match=f"incorrect cutting range {1} - {1}"):
        initial[1:1]


def test_getslice_lower():
    lower = 1
    initial = PLFunction([(0, 0), (10, 100)])
    cut = initial[lower:]
    assert cut.min_x == lower
    assert cut.max_x == initial.max_x
    assert cut[lower] == 10
    assert cut[initial.max_x] == 100


def test_getslice_upper():
    upper = 9
    initial = PLFunction([(0, 0), (10, 100)])
    cut = initial[:upper]
    assert cut.min_x == initial.min_x
    assert cut.max_x == upper
    assert cut[initial.min_x] == 0
    assert cut[upper] == 90


def test_getslice():
    lower = 1
    upper = 9
    initial = PLFunction([(0, 0), (10, 100)])
    cut = initial[lower:upper]
    assert cut.min_x == lower
    assert cut.max_x == upper
    assert cut[lower] == 10
    assert cut[upper] == 90


def test_wider_getslice():
    initial = PLFunction([(0, 0), (10, 100)])
    cut = initial[-10:20]
    assert initial.xp == cut.xp
    assert initial.fp == cut.fp


def test_defined_out_of_range_raises(pl: PLFunction):
    with pytest.raises(
        ValueError, match=f"x should be in range {pl.min_x} - {pl.max_x}"
    ):
        pl.defined_f(-2)


def test_defined(pl: PLFunction, x, x_exp_def):
    assert pl.defined_f(x) == x_exp_def


def test_intersects_simple():
    a = PLFunction([(0, 0), (1, 1)])
    b = PLFunction([(1, 0), (0, 1)])
    assert a.overlaps_with(b)


def test_touches_simple():
    a = PLFunction([(0, 0), (1, 1)])
    b = PLFunction([(0, 0), (1, 10)])
    assert a.overlaps_with(b)


def test_intersects_false_min():
    a = PLFunction([(0, 0), (1, 1)])
    b = PLFunction([(-1, 0), (-2, 1)])
    assert not a.overlaps_with(b)


def test_intersects_false_max():
    a = PLFunction([(0, 0), (1, 1)])
    b = PLFunction([(2, 0), (3, 1)])
    assert not a.overlaps_with(b)


def test_intersects_complex():
    a = PLFunction([(0, 0), (1, 5), (2, 5), (10, 100)])
    b = PLFunction([(1.1, 4), (1.8, 6)])
    assert a.overlaps_with(b)
