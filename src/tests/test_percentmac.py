import pytest
from wbkit.basic import Index, IndexConstants, PercentMAC


def test_init(lemac_at: float, macrc_length: float):
    pctmac = PercentMAC(13.52, lemac_at, macrc_length)
    assert pctmac.value == 13.52
    assert pctmac.lemac_at == lemac_at
    assert pctmac.macrc_length == macrc_length


@pytest.mark.parametrize(
    [
        "idx_value",
        "weight",
        "pctmac_value",
        "rck",
        "lemac_at",
        "macrc_length",
    ],
    [
        (61.84, 14007, 35.42, "rck", "lemac_at", "macrc_length"),
        (49.81, 14434, 25.90, "rck", "lemac_at", "macrc_length"),
        (29.84, 17841, 13.52, "rck", "lemac_at", "macrc_length"),
        (23.72, 21627, 12.58, "rck", "lemac_at", "macrc_length"),
        (23.83, 20354, 11.80, "rck", "lemac_at", "macrc_length"),
    ],
    indirect=["rck", "lemac_at", "macrc_length"],
)
def test_from_idx(
    idx_value: float,
    weight: int,
    pctmac_value: float,
    rck: IndexConstants,
    lemac_at: float,
    macrc_length: float,
):
    idx = Index(idx_value, weight, rck)
    pctmac = PercentMAC.from_idx(idx, lemac_at, macrc_length)
    assert pctmac.value == pytest.approx(pctmac_value, 1e-3)
    assert pctmac.lemac_at == lemac_at
    assert pctmac.macrc_length == macrc_length


@pytest.mark.parametrize(
    [
        "idx_value",
        "weight",
        "pctmac_value",
        "rck",
        "lemac_at",
        "macrc_length",
    ],
    [
        (29.84, 17841, 13.52, "rck", "lemac_at", "macrc_length"),
        (23.72, 21627, 12.58, "rck", "lemac_at", "macrc_length"),
        (23.83, 20354, 11.80, "rck", "lemac_at", "macrc_length"),
    ],
    indirect=["rck", "lemac_at", "macrc_length"],
)
def test_to_idx(
    idx_value: float,
    weight: int,
    pctmac_value: float,
    rck: IndexConstants,
    lemac_at: float,
    macrc_length: float,
):
    pctmac = PercentMAC(pctmac_value, lemac_at, macrc_length)
    exp_idx = Index(idx_value, weight, rck)
    idx = pctmac.to_idx(weight, rck)
    assert idx.idx == pytest.approx(exp_idx.idx, 1e-3)
    assert idx.weight == exp_idx.weight
    assert idx.rck == exp_idx.rck
