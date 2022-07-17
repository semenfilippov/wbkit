import pytest
from wbkit.cglimits import CG, CGLimits
from wbkit.plfunc import PLFunction


class TestInit:
    def test_diff_fwd(self, invalid_fwd_line, zfw_aft_line):
        with pytest.raises(
            ValueError,
            match="fwd_line and aft_line min and max weights should be equal",
        ):
            CGLimits(invalid_fwd_line, zfw_aft_line)

    def test_diff_aft(self, zfw_fwd_line, invalid_aft_line):
        with pytest.raises(
            ValueError,
            match="fwd_line and aft_line min and max weights should be equal",
        ):
            CGLimits(zfw_fwd_line, invalid_aft_line)

    def test_wrong_order(self, zfw_fwd_line, zfw_aft_line):
        with pytest.raises(ValueError, match="make sure order of lines is fwd, aft"):
            CGLimits(zfw_aft_line, zfw_fwd_line)

    def test_intersecting_lines(self):
        with pytest.raises(
            ValueError, match="fwd_line and aft_line should not overlap"
        ):
            CGLimits(PLFunction([(0, 0), (10, 10)]), PLFunction([(0, 10), (10, 0)]))

    def test_init_with_tuples(self):
        fwd_points = [(13500, 20), (19900, 10)]
        aft_points = [(13500, 50), (19900, 60)]
        limits = CGLimits(fwd_points, aft_points)
        assert all([x == y for x, y in zip(fwd_points, limits.fwd.points)])


class TestProps:
    def test_min_weight(self, zfw_cglimits: CGLimits):
        assert zfw_cglimits.min_weight == 13608

    def test_max_weight(self, zfw_cglimits: CGLimits):
        assert zfw_cglimits.max_weight == 19958


class TestCut:
    def test_cut_range_max(self, zfw_cglimits: CGLimits):
        new_limits = zfw_cglimits.cut_weight_range(max=19000)
        assert new_limits.max_weight == 19000

    def test_cut_range_min(self, zfw_cglimits: CGLimits):
        new_limits = zfw_cglimits.cut_weight_range(min=14000)
        assert new_limits.min_weight == 14000

    def test_cut_range(self, zfw_cglimits: CGLimits):
        new_limits = zfw_cglimits.cut_weight_range(14000, 19000)
        assert new_limits.min_weight == 14000
        assert new_limits.max_weight == 19000


class TestRange:
    def test_lt_min_is_none(self, zfw_cglimits: CGLimits):
        assert zfw_cglimits.limit_range(13000) is None

    def test_gt_max_is_none(self, zfw_cglimits: CGLimits):
        assert zfw_cglimits.limit_range(20000) is None

    def test_in_range(self, zfw_cglimits: CGLimits):
        assert zfw_cglimits.limit_range(13608) == (34.45, 57.31)


class TestContains:
    def test_good_idx(self, zfw_cglimits: CGLimits, good_idx: CG):
        assert good_idx in zfw_cglimits

    def test_bad_fwd_idx(self, zfw_cglimits: CGLimits, bad_fwd_idx: CG):
        assert bad_fwd_idx not in zfw_cglimits

    def test_bad_aft_idx(self, zfw_cglimits: CGLimits, bad_aft_idx: CG):
        assert bad_aft_idx not in zfw_cglimits


class TestExceedsFwd:
    def test_good_idx(self, zfw_cglimits: CGLimits, good_idx: CG):
        assert not zfw_cglimits.exceeds_fwd(good_idx.value, good_idx.weight)

    def test_bad_fwd_idx(self, zfw_cglimits: CGLimits, bad_fwd_idx: CG):
        assert zfw_cglimits.exceeds_fwd(bad_fwd_idx.value, bad_fwd_idx.weight)

    def test_bad_aft_idx(self, zfw_cglimits: CGLimits, bad_aft_idx: CG):
        assert not zfw_cglimits.exceeds_fwd(bad_aft_idx.value, bad_aft_idx.weight)

    def test_bad_weight_idx(self, zfw_cglimits: CGLimits, bad_weight_idx: CG):
        assert zfw_cglimits.exceeds_fwd(bad_weight_idx.value, bad_weight_idx.weight)


class TestExceedsAft:
    def test_good_idx(self, zfw_cglimits: CGLimits, good_idx: CG):
        assert not zfw_cglimits.exceeds_aft(good_idx.value, good_idx.weight)

    def test_bad_fwd_idx(self, zfw_cglimits: CGLimits, bad_fwd_idx: CG):
        assert not zfw_cglimits.exceeds_aft(bad_fwd_idx.value, bad_fwd_idx.weight)

    def test_bad_aft_idx(self, zfw_cglimits: CGLimits, bad_aft_idx: CG):
        assert zfw_cglimits.exceeds_aft(bad_aft_idx.value, bad_aft_idx.weight)

    def test_bad_weight_idx(self, zfw_cglimits: CGLimits, bad_weight_idx: CG):
        assert zfw_cglimits.exceeds_aft(bad_weight_idx.value, bad_weight_idx.weight)


class TestCGExceedsFwd:
    def test_good_idx(self, zfw_cglimits: CGLimits, good_idx: CG):
        assert not zfw_cglimits.cg_exceeds_fwd(good_idx)

    def test_bad_fwd_idx(self, zfw_cglimits: CGLimits, bad_fwd_idx: CG):
        assert zfw_cglimits.cg_exceeds_fwd(bad_fwd_idx)

    def test_bad_aft_idx(self, zfw_cglimits: CGLimits, bad_aft_idx: CG):
        assert not zfw_cglimits.cg_exceeds_fwd(bad_aft_idx)

    def test_bad_weight_idx(self, zfw_cglimits: CGLimits, bad_weight_idx: CG):
        assert zfw_cglimits.cg_exceeds_fwd(bad_weight_idx)


class TestCGExceedsAft:
    def test_good_idx(self, zfw_cglimits: CGLimits, good_idx: CG):
        assert not zfw_cglimits.cg_exceeds_aft(good_idx)

    def test_bad_fwd_idx(self, zfw_cglimits: CGLimits, bad_fwd_idx: CG):
        assert not zfw_cglimits.cg_exceeds_aft(bad_fwd_idx)

    def test_bad_aft_idx(self, zfw_cglimits: CGLimits, bad_aft_idx: CG):
        assert zfw_cglimits.cg_exceeds_aft(bad_aft_idx)

    def test_bad_weight_idx(self, zfw_cglimits: CGLimits, bad_weight_idx: CG):
        assert zfw_cglimits.cg_exceeds_aft(bad_weight_idx)
