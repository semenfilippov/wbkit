"""
Weight and balance calculation module.
"""
from collections import namedtuple
from fuel import get_closest_fuel_index
from basic import calc_macrc


AircraftConfig = namedtuple(
    "AircraftConfig",
    [
        "dow",
        "doi",
        "mzfw",
        "mtow",
        "mlw",
        "a_capacity",
        "b_capacity",
        "c_capacity",
        "d_capacity",
        "a_influence",
        "b_influence",
        "c_influence",
        "d_influence",
        "cargo_influence",
    ],
)

WeightConfig = namedtuple("WeightConfig", ["adult", "child", "infant"])
TripInfo = namedtuple("TripInfo", ["takeoff_fuel", "trip_fuel"])

PayloadData = namedtuple(
    "Payload",
    [
        "adults",
        "children",
        "infants",
        "cabin_baggage",
        "cargo",
        "pax_a",
        "pax_b",
        "pax_c",
        "pax_d",
    ],
)


def calculate(
    aircraft: AircraftConfig,
    weight: WeightConfig,
    trip_info: TripInfo,
    payload: PayloadData,
):
    operating_weight = aircraft.dow + trip_info.takeoff_fuel
    allowed_tow = min(
        aircraft.mtow,
        aircraft.mzfw + trip_info.takeoff_fuel,
        aircraft.mlw + trip_info.trip_fuel,
    )
    allowed_traffic_load = allowed_tow - operating_weight
    total_traffic_load = (
        payload.adults * weight.adult
        + payload.children * weight.child
        + payload.infants * weight.infant
        + payload.cabin_baggage
        + payload.cargo
    )
    # TODO: check for negative value
    underload_lmc = allowed_traffic_load - total_traffic_load
    zfw = aircraft.dow + total_traffic_load
    tow = zfw + trip_info.takeoff_fuel
    ldw = tow - trip_info.trip_fuel
    lizfw = (
        aircraft.doi
        + payload.cargo * aircraft.cargo_influence
        + payload.pax_a * weight.adult * aircraft.a_influence
        + payload.pax_b * weight.adult * aircraft.b_influence
        + payload.pax_c * weight.adult * aircraft.c_influence
        + payload.pax_d * weight.adult * aircraft.d_influence
    )
    litow = lizfw + get_closest_fuel_index(trip_info.takeoff_fuel)
    lilaw = lizfw + get_closest_fuel_index(trip_info.takeoff_fuel - trip_info.trip_fuel)
    maczfw = calc_macrc(lizfw, zfw)
    mactow = calc_macrc(litow, tow)
    macldw = calc_macrc(lilaw, ldw)
    print(
        f"LIZFW {round(lizfw, 2)}\nLITOW {round(litow, 2)}\nLILAW {round(lilaw, 2)}\n"
        f"MACZFW {round(maczfw, 2)}\nMACTOW {round(mactow, 2)}\n"
        f"MACLDW {round(macldw, 2)}"
    )


if __name__ == "__main__":
    # should be fetched from db
    aircraft_config = AircraftConfig(
        dow=14434,
        doi=49.81,
        mzfw=19958,
        mtow=24040,
        mlw=21319,
        a_capacity=16,
        b_capacity=12,
        c_capacity=12,
        d_capacity=10,
        a_influence=-0.01997,
        b_influence=-0.01013,
        c_influence=-0.00161,
        d_influence=0.00627,
        cargo_influence=0.01547,
    )
    weight_config = WeightConfig(adult=75, child=30, infant=15)
    trip_info = TripInfo(takeoff_fuel=3786, trip_fuel=1771)
    payload_data = PayloadData(
        adults=41,
        children=2,
        infants=0,
        cabin_baggage=91,
        cargo=181,
        pax_a=12,
        pax_b=12,
        pax_c=9,
        pax_d=10,
    )
    calculate(aircraft_config, weight_config, trip_info, payload_data)
