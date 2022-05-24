from typing import Dict, Union
from crjwb.basic import Interpolatable


class FuelEffect(Interpolatable):
    def __init__(self, points: Dict[int, Union[int, float]]) -> None:
        """Get new FuelEffect object.

        Args:
            points (Dict[int, Union[int, float]]): fuel effect index influence points,
            where key is fuel quantity, value is index influence
        """
        super().__init__(points)

    def get_influence(self, fuel: int, allow_interpolation: bool = False) -> float:
        """Get index influence for given fuel quantity.

        Args:
            `fuel` (int): fuel quantity
            `allow_interpolation` (bool, optional): Whether to interpolate
            index influence or not.
            Defaults to False.

        Returns:
            `float`: index influence
        """
        if allow_interpolation:
            return self.get_interpolated_value(fuel)
        return self.get_defined_value(fuel)
