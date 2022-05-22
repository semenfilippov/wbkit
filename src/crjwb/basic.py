class BasicCalc:
    def __init__(
        self,
        ref_station: float,
        k_constant: int,
        c_constant: int,
        macrc_length: float,
        lemac_at: float,
    ) -> None:
        """Initialize BasicCalc.

        Args:
            ``ref_station`` (float): Reference station/axis. Selected station \
                around which all index values are calculated.
            ``k_constant`` (int): Constant used as a plus value to avoid \
                negative index figures.
            ``c_constant`` (int): Constant used as a denominator to convert \
                moment values into index values.
            ``macrc_length`` (float): Length of \
                Mean Aerodynamic Chord / Reference Chord in length units.
            ``lemac_at`` (float): Horizontal distance in length units \
                from the station zero to location of the Leading Edge of the MAC / RC.
        """
        self.ref_station = ref_station
        self.k_constant = k_constant
        self.c_constant = c_constant
        self.macrc_length = macrc_length
        self.lemac_at = lemac_at

    def calc_index(self, weight: float, station: float) -> float:
        """Calculate index.

        Parameters
        ----------
        ``weight`` (float): actual weight
        ``station`` (float): horizontal distance in meters
        from station zero to the location

        Returns
        ----------
        ``float``: index
        """
        return float(
            (weight * (station - self.ref_station)) / self.c_constant + self.k_constant
        )

    def calc_macrc(self, idx: float, weight: float) -> float:
        """Calculate MAC/RC.

        Parameters
        ----------
        ``idx`` (float): index value corresponding to respective weight
        ``weight`` (float): actual weight

        Returns
        ----------
        ``float``: MAC/RC
        """
        return (
            ((self.c_constant * (idx - self.k_constant)) / weight)
            + self.ref_station
            - self.lemac_at
        ) / (self.macrc_length / 100)
