from typing import Dict, Union
from numpy import interp


class Stab:
    """Stabilizer trim calculator"""

    def __init__(self, points: Dict[Union[int, float], Union[int, float]]) -> None:
        """Get new stabilizer trim calculator.

        Args:
            ``points`` (Dict[int | float, int | float]): stab trim function points,
            where keys are MAC/RC values, values are corresponding stab trim settings

        Raises:
            ValueError: if ``points`` length is less than 2
        """
        if len(points) < 2:
            raise ValueError("You should provide at least two points!")
        self.xp = sorted([x for x in points])
        self.xp_min = min(self.xp)
        self.xp_max = max(self.xp)
        self.fp = [points[x] for x in self.xp]

    def calc(self, mactow: float) -> float:
        """Get takeoff stab trim setting for given %MAC.

        Args:
            mactow (float): %MAC/RC for TOW

        Raises:
            ValueError: if mactow is outside of defined range

        Returns:
            float: stab trim setting
        """
        if mactow < self.xp_min or mactow > self.xp_max:
            raise ValueError(f"MACTOW should be within {self.xp_min}% - {self.xp_max}%")
        return interp(mactow, self.xp, self.fp)
