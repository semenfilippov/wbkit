from wbkit.config import FuelEffect, StabRange, WBConfig


def test_config(zfw_cglimits):
    class CRJ(WBConfig):
        zf = zfw_cglimits

    class CRJ200(CRJ):
        a = StabRange([(8.8, 8.15), (35, 4)])
        fuel = FuelEffect([(0, 0), (6000, -17)])

    crj = CRJ200()
    assert crj.cglimits["zf"] == zfw_cglimits
    assert crj.stab["a"][8.8] == 8.15
    assert crj.fuel[6000] == -17
