from typing import Any, Dict
from wbkit.interpolables import Interpolable
from wbkit.cglimits import CGLimits


class FuelEffect(Interpolable):
    "Fuel index influence."


class StabRange(Interpolable):
    """Stab trim range representation."""


class WBConfigBase(type):
    cglimits: Dict[str, CGLimits]
    fuel: FuelEffect
    stab: Dict[str, StabRange]

    def __new__(cls, name, bases, attrs: Dict[str, Any]):
        if name is None:
            return None

        new_attrs: Dict[str, Any] = {}
        new_attrs["stab"] = {}
        new_attrs["fuel"] = None
        new_attrs["cglimits"] = {}

        for baseclass in bases:  # not sure if this is correct, but it works
            if isinstance(baseclass, cls):
                new_attrs["cglimits"].update(baseclass.cglimits)
                new_attrs["fuel"] = baseclass.fuel
                new_attrs["stab"].update(baseclass.stab)

        for k, v in attrs.items():
            if isinstance(v, CGLimits):
                new_attrs["cglimits"][k] = v
                continue
            if isinstance(v, FuelEffect):
                new_attrs["fuel"] = v
                continue
            if isinstance(v, StabRange):
                new_attrs["stab"][k] = v
                continue
            new_attrs[k] = v

        return super().__new__(cls, name, bases, new_attrs)


class WBConfig(metaclass=WBConfigBase):
    cglimits: Dict[str, CGLimits]
    fuel: FuelEffect
    stab: Dict[str, StabRange]
