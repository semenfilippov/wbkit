from typing import Dict, Union


class FuelEffect:
    def __init__(self, fuel_effect: Dict[int, Union[int, float]]) -> None:
        """Construct new FuelEffect object.

        Parameters
        ----------
        ``fuel_effect`` (Dict[int, int | float]]): keys are fuel quantities,
        values are their index influencies

        Raises
        ----------
        ValueError: if fuel_effect is empty
        """
        if not fuel_effect:
            raise ValueError(
                "Argument fuel_effect must constist at least of one key value pair"
            )
        self.fuel_effect = fuel_effect
        self.min_fuel = min(self.fuel_effect)
        self.max_fuel = max(self.fuel_effect)

    def get_min_fuel(self) -> int:
        """Get minimum fuel quantity FuelEffect object is able
        to give index influence for.

        Returns
        ----------
        int: fuel quantity
        """
        return self.min_fuel

    def get_max_fuel(self) -> int:
        """Get maximum fuel quantity FuelEffect object is able
        to give index influence for.

        Returns
        ----------
        int: fuel quantity
        """
        return self.max_fuel

    def get_influence(self, fuel: int) -> float:
        """Get closest fuel index.

        Parameters
        ----------
        fuel (int): fuel quantity

        Raises
        ----------
        ValueError: if fuel value is negative
        ValueError: if fuel value exceeds maximum

        Returns
        ----------
        float: index influence
        """
        if fuel in self.fuel_effect:
            return self.fuel_effect[fuel]
        if fuel < self.min_fuel:
            raise ValueError(
                f"Incorrect fuel value: {fuel} (must not be less than {self.min_fuel})."
            )
        if fuel > self.max_fuel:
            raise ValueError(
                f"Incorrect fuel value: {fuel} (must not exceed {self.max_fuel})."
            )
        min_diff = min({abs(fuel - x) for x in self.fuel_effect})
        possible_indexes = [
            self.fuel_effect[x]
            for x in {fuel + min_diff, fuel - min_diff}
            if x in self.fuel_effect
        ]
        if len(possible_indexes) > 1:
            return (
                possible_indexes[0]
                if abs(possible_indexes[0]) >= abs(possible_indexes[1])
                else possible_indexes[1]
            )
        return possible_indexes[0]
