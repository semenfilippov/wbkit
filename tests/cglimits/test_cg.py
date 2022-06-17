import pytest
from wbkit.cglimits import CG


@pytest.mark.parametrize("cg", [CG(0, 0)])
class TestNoLimitsRaises:
    def test_limits(self, cg: CG):
        with pytest.raises(TypeError, match="CG object has no assigned limits"):
            cg.in_limits

    def test_limit_range(self, cg: CG):
        with pytest.raises(TypeError, match="CG object has no assigned limits"):
            cg.limit_range

    def test_exceeds_fwd(self, cg: CG):
        with pytest.raises(TypeError, match="CG object has no assigned limits"):
            cg.exceeds_fwd

    def test_exceeds_aft(self, cg: CG):
        with pytest.raises(TypeError, match="CG object has no assigned limits"):
            cg.exceeds_aft


class TestInLimits:
    def test_good(self, good_idx: CG):
        assert good_idx.in_limits

    def test_bad_fwd_idx(self, bad_fwd_idx: CG):
        assert not bad_fwd_idx.in_limits

    def test_bad_aft_idx(self, bad_aft_idx: CG):
        assert not bad_aft_idx.in_limits

    def test_bad_weight_idx(self, bad_weight_idx: CG):
        assert not bad_weight_idx.in_limits


class TestExceedsFwd:
    def test_good(self, good_idx: CG):
        assert not good_idx.exceeds_fwd

    def test_bad_fwd_idx(self, bad_fwd_idx: CG):
        assert bad_fwd_idx.exceeds_fwd

    def test_bad_aft_idx(self, bad_aft_idx: CG):
        assert not bad_aft_idx.exceeds_fwd

    def test_bad_weight_idx(self, bad_weight_idx: CG):
        assert bad_weight_idx.exceeds_fwd


class TestExceedsAft:
    def test_good(self, good_idx: CG):
        assert not good_idx.exceeds_aft

    def test_bad_fwd_idx(self, bad_fwd_idx: CG):
        assert not bad_fwd_idx.exceeds_aft

    def test_bad_aft_idx(self, bad_aft_idx: CG):
        assert bad_aft_idx.exceeds_aft

    def test_bad_weight_idx(self, bad_weight_idx: CG):
        assert bad_weight_idx.exceeds_aft


class TestLimitRange:
    def test_good(self, good_idx: CG):
        assert good_idx.limit_range is not None
        assert len(good_idx.limit_range) == 2

    def test_bad_weight_idx(self, bad_weight_idx: CG):
        assert bad_weight_idx.limit_range is None
