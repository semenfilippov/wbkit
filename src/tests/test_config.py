from wbkit.config import (
    FuelEffect,
    StabRange,
    WBConfig,
    PassengerLocation,
    CargoLocation,
)


def test_config(zfw_cglimits):
    class CRJ(WBConfig):
        zf = zfw_cglimits

    class CRJ200(CRJ):
        all = StabRange([(8.8, 8.15), (35, 4)])
        fuel = FuelEffect([(0, 0), (6000, -17)])
        a = PassengerLocation(-0.1013, 16)
        aft = CargoLocation(0.16, 1500)

    crj = CRJ200()
    assert crj.cglimits["zf"] == zfw_cglimits
    assert crj.stabs["all"][8.8] == 8.15
    assert crj.stab[35] == 4
    assert crj.fuel[6000] == -17
    assert crj.paxlocs["a"].capacity == 16
    assert crj.paxlocs["a"].influence == -0.1013
    assert crj.cargolocs["aft"].influence == 0.16
    assert crj.cargolocs["aft"].max_weight == 1500
