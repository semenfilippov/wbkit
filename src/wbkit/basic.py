class WBCalculator:
    def __init__(
        self, ref_st: float, c: int, k: int, macrc: float, lemac_at: float
    ) -> None:
        """Create new WBCalculator object.

        Args:
            ref_st (float): Reference station/axis. Selected station
            around which all index values are calculated.
            c (int): Constant used as a denominator to convert
            moment values into index values.
            k (int): Constant used as a plus value to avoid
            negative index figures.
            lemac_at (float): Horizontal distance in length units
            from the station zero to location of the Leading Edge of the MAC / RC
            macrc_length (float): Length of
            Mean Aerodynamic Chord / Reference Chord in length units.

        Raises:
            ValueError: if C constant is not > 0
            ValueError: if K constant is < 0
            ValueError: if MAC/RC length not > 0
        """
        if not c > 0:
            raise ValueError("C constant must be > 0")
        if k < 0:
            raise ValueError("K constant must not be negative")
        if not macrc > 0:
            raise ValueError("MAC/RC must be > 0")
        self.ref_st = ref_st
        self.c = c
        self.k = k
        self.macrc = macrc
        self.lemac_at = lemac_at

    def to_idx(self, moment: float) -> float:
        """Convert moment to index.

        Args:
            moment (float): moment

        Returns:
            float: index
        """
        return moment / self.c + self.k

    def to_moment(self, idx: float) -> float:
        """Convert index to moment.

        Args:
            idx (float): index

        Returns:
            float: index
        """
        return self.c * (idx - self.k)

    def calc_moment(self, weight: int, station: float) -> float:
        """Calculate moment for given weight and station.

        Args:
            weight (int): weight
            station (float): station

        Returns:
            float: moment
        """
        return weight * (station - self.ref_st)

    def calc_idx(self, weight: int, station: float) -> float:
        """Calculate index for given weight and station.

        Args:
            weight (int): weight
            station (float): station

        Returns:
            float: index
        """
        return self.to_idx(self.calc_moment(weight, station))

    def mac_from_moment(self, moment: float, weight: int) -> float:
        """Get %MAC for given moment and weight.

        Args:
            moment (float): moment
            weight (int): weight

        Returns:
            float: %MAC
        """
        try:
            return (moment / weight + self.ref_st - self.lemac_at) / (self.macrc / 100)
        except ZeroDivisionError:
            raise ValueError("weight must not be equal to 0")

    def mac_to_moment(self, mac: float, weight: int) -> float:
        """Get moment for given %MAC and weight.

        Args:
            mac (float): %MAC
            weight (int): weight

        Returns:
            float: moment
        """
        return ((mac * (self.macrc / 100)) - self.ref_st + self.lemac_at) * weight

    def mac_from_idx(self, idx: float, weight: int) -> float:
        """Get %MAC for given index and weight.

        Args:
            idx (float): index
            weight (int): weight

        Returns:
            float: %MAC
        """
        return self.mac_from_moment(self.to_moment(idx), weight)

    def mac_to_idx(self, mac: float, weight: int) -> float:
        """Get index for given %MAC and weight.

        Args:
            mac (float): %MAC
            weight (int): weight

        Returns:
            float: index
        """
        return self.to_idx(self.mac_to_moment(mac, weight))
