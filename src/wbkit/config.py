from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from wbkit.cglimits import CGLimits
from wbkit.interpolables import Interpolable


class Location(ABC):
    @abstractmethod
    def __init__(self, influence: float) -> None:
        self.influence = influence


class PassengerLocation(Location):
    def __init__(self, influence: float, capacity: int) -> None:
        super().__init__(influence)
        self.capacity = capacity


class CargoLocation(Location):
    def __init__(self, influence: float, max_weight: int) -> None:
        super().__init__(influence)
        self.max_weight = max_weight


class FuelEffect(Interpolable):
    "Fuel index influence."


class StabRange(Interpolable):
    """Stab trim range representation."""


class WBConfigBase(type):
    cargolocs: Dict[str, CargoLocation]
    cglimits: Dict[str, CGLimits]
    fuel: Optional[FuelEffect]
    paxlocs: Dict[str, PassengerLocation]
    stabs: Dict[str, StabRange]

    def __new__(cls, name, bases, attrs: Dict[str, Any]):
        if name is None:
            return None

        new_attrs: Dict[str, Any] = {}
        new_attrs["cargolocs"] = {}
        new_attrs["cglimits"] = {}
        new_attrs["fuel"] = None
        new_attrs["paxlocs"] = {}
        new_attrs["stabs"] = {}

        for baseclass in bases:  # not sure if this is correct, but it works
            if isinstance(baseclass, cls):
                new_attrs["cglimits"].update(baseclass.cglimits)
                new_attrs["fuel"] = baseclass.fuel
                new_attrs["stabs"].update(baseclass.stabs)

        for k, v in attrs.items():
            if isinstance(v, CargoLocation):
                new_attrs["cargolocs"][k] = v
                continue
            if isinstance(v, CGLimits):
                new_attrs["cglimits"][k] = v
                continue
            if isinstance(v, FuelEffect):
                new_attrs["fuel"] = v
                continue
            if isinstance(v, PassengerLocation):
                new_attrs["paxlocs"][k] = v
                continue
            if isinstance(v, StabRange):
                new_attrs["stabs"][k] = v
                continue
            new_attrs[k] = v

        return super().__new__(cls, name, bases, new_attrs)


class WBConfig(metaclass=WBConfigBase):
    cargolocs: Dict[str, CargoLocation]
    cglimits: Dict[str, CGLimits]
    fuel: Optional[FuelEffect]
    paxlocs: Dict[str, PassengerLocation]
    stabs: Dict[str, StabRange]

    @property
    def stab(self) -> Optional[StabRange]:
        if len(self.stabs) == 1:
            return next(iter(self.stabs.values()))
        return None
