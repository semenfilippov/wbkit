import pytest
from wbkit.basic import WBCalculator


@pytest.fixture(scope="class")
def wbcalc():
    return WBCalculator(10, 2, 10, 10, 10)


class TestSimple:
    def test_init(self):
        wbcalc = WBCalculator(13.2, 280, 50, 2.526, 12.542)
        assert wbcalc.ref_st == 13.2
        assert wbcalc.c == 280
        assert wbcalc.k == 50
        assert wbcalc.macrc == 2.526
        assert wbcalc.lemac_at == 12.542

    @pytest.mark.parametrize("c", [(0), (-1)])
    def test_zero_or_negative_c_raises(self, c):
        with pytest.raises(ValueError, match="C constant must be > 0"):
            WBCalculator(13.2, c, 50, 2.526, 12.542)

    def test_negative_k_raises(self):
        with pytest.raises(ValueError, match="K constant must not be negative"):
            WBCalculator(13.2, 280, -1, 2.526, 12.542)

    def test_to_idx(self, wbcalc: WBCalculator):
        assert wbcalc.to_idx(10) == 15

    def test_to_moment(self, wbcalc: WBCalculator):
        assert wbcalc.to_moment(15) == 10

    def test_calc_moment(self, wbcalc: WBCalculator):
        assert wbcalc.calc_moment(10, 20) == 100

    def test_calc_idx(self, wbcalc: WBCalculator):
        assert wbcalc.calc_idx(10, 20) == 60

    def test_mac_from_moment(self, wbcalc: WBCalculator):
        assert wbcalc.mac_from_moment(100, 20) == 50.0

    def test_mac_from_moment_zero_weight_raises(self, wbcalc: WBCalculator):
        with pytest.raises(ValueError, match="weight must not be equal to 0"):
            wbcalc.mac_from_moment(100, 0)

    def test_moment_from_mac(self, wbcalc: WBCalculator):
        assert wbcalc.mac_to_moment(50.0, 20) == 100

    def test_mac_from_idx(self, wbcalc: WBCalculator):
        assert wbcalc.mac_from_idx(60, 20) == 50

    def test_mac_to_idx(self, wbcalc: WBCalculator):
        assert wbcalc.mac_to_idx(50, 20) == 60

    # some real examples


@pytest.mark.parametrize("calc", [WBCalculator(13.2, 280, 50, 2.526, 12.542)])
class TestReal:
    @pytest.mark.parametrize(
        "idx, weight, mac",
        [
            (29.84, 17841, 13.52),
            (23.72, 21627, 12.58),
            (23.83, 20354, 11.80),
        ],
    )
    def test_mac_from_idx(self, calc, idx, weight, mac):
        assert calc.mac_from_idx(idx, weight) == pytest.approx(mac, 1e-3)

    @pytest.mark.parametrize(
        "idx, weight, mac",
        [
            (29.84, 17841, 13.52),
            (23.72, 21627, 12.58),
            (23.83, 20354, 11.80),
        ],
    )
    def test_mac_to_idx(self, calc, idx, weight, mac):
        assert calc.mac_to_idx(mac, weight) == pytest.approx(idx, 1e-3)
