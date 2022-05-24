from crjwb.basic import Interpolable, LinearFuncPoints


class Stab(Interpolable):
    """Stabilizer trim calculator"""

    def __init__(self, points: LinearFuncPoints) -> None:
        """Get new stabilizer trim calculator.

        Args:
            points (Dict[int, Union[int, float]]): stab trim function points,
            where keys are MAC/RC values, values are corresponding stab trim settings
        """
        super().__init__(points)

    def calc(self, mactow: float) -> float:
        """Get takeoff stab trim setting for given %MAC.

        Args:
            mactow (float): %MAC/RC for TOW

        Returns:
            float: stab trim setting
        """
        return self.get_interpolated_value(mactow)
