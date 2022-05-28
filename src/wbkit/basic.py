class Index:
    """Moment index representation."""

    def __init__(self, idx: float, weight: int, ref_st: float, c: int, k: int) -> None:
        """Create new Index object.

        Args:
            idx (float): Index value
            weight (int): Corresponding weight
            ref_st (float): Reference station/axis. Selected station
            around which all index values are calculated
            c (int): Constant used as a denominator to convert
            moment values into index values
            k (int): Constant used as a plus value to avoid
            negative index figures

        Raises:
            ValueError: if `c` equals to 0
        """
        if not c > 0:
            raise ValueError("C constant should be greater than 0")
        if k < 0:
            raise ValueError("K constant should not be negative")
        self.value = idx
        self.weight = weight
        self.ref_st = ref_st
        self.c = c
        self.k = k

    @property
    def moment(self) -> float:
        """Get moment value.

        Returns:
            float: moment
        """
        return (self.value - self.k) * self.c

    @staticmethod
    def calc(weight: int, station: float, ref_st: float, c: int, k: int):
        """Calculate index value and return Index object.

        Args:
            weight (int): Actual weight
            station (float): Horizontal distance in length units
            from station zero to the location
            ref_st (float): Reference station/axis. Selected station
            around which all index values are calculated
            c (int): Constant used as a denominator to convert
            moment values into index values
            k (int): Constant used as a plus value to avoid
            negative index figures

        Raises:
            ValueError: if `c` equals to zero

        Returns:
            Index: calculated Index object
        """
        try:
            idx = (weight * (station - ref_st)) / c + k
        except ZeroDivisionError:
            raise ValueError("C constant cannot be equal to 0")
        return Index(idx, weight, ref_st, c, k)

    def __validate_calc_ops__(self, other):
        """Internal Index object validator.
        Validate if two Index objects can be added or substracted.
        It is only possible when their `ref_st`, `c` and `k`
        attributes are equal.

        Args:
            other (Index): Index object

        Raises:
            ValueError: if either of `ref_st`, `c` or `k` Index object
            attributes are not equal
        """
        if self.ref_st == other.ref_st and self.c == other.c and self.k == other.k:
            return

        raise ValueError(
            "Calculations for Index operands with different "
            "reference stations, C or K constants are not allowed."
        )

    def __validate_compare_ops__(self, other):
        """Internal Index object validator.
        Validate if two Index objects can compared.
        It is only possible when their `ref_st` attributes are equal.

        Args:
            other (Index): Index object

        Raises:
            ValueError: if `ref_st` attributes are not equal
        """
        if not self.ref_st == other.ref_st:
            raise ValueError(
                "Cannot compare Index instances with different reference stations."
            )

    def __add__(self, other):
        self.__validate_calc_ops__(other)
        sum_weights = self.weight + other.weight
        sum_idxs = self.value + other.value
        return Index(sum_idxs, sum_weights, self.ref_st, self.c, self.k)

    def __sub__(self, other):
        self.__validate_calc_ops__(other)
        sum_weights = self.weight - other.weight
        sum_idxs = self.value - other.value
        return Index(sum_idxs, sum_weights, self.ref_st, self.c, self.k)

    def __mul__(self, other):
        return Index(
            self.value * other, self.weight * other, self.ref_st, self.c, self.k
        )

    def __eq__(self, other):
        self.__validate_compare_ops__(other)
        return self.moment == other.moment

    def __gt__(self, other):
        self.__validate_compare_ops__(other)
        return self.moment > other.moment

    def __lt__(self, other):
        self.__validate_compare_ops__(other)
        return self.moment < other.moment

    def __ge__(self, other):
        self.__validate_compare_ops__(other)
        return self > other or self == other

    def __le__(self, other):
        self.__validate_compare_ops__(other)
        return self < other or self == other


class PercentMAC:
    """%MAC representation."""

    def __init__(self, value: float, lemac_at: float, macrc_length: float) -> None:
        """Create new PercentMAC object.

        Args:
            value (float): %MAC value
            lemac_at (float): Horizontal distance in length units
            from the station zero to location of the Leading Edge of the MAC / RC
            macrc_length (float): Length of
            Mean Aerodynamic Chord / Reference Chord in length units
        """
        self.value = value
        self.lemac_at = lemac_at
        self.macrc_length = macrc_length

    @staticmethod
    def from_idx(idx: Index, lemac_at: float, macrc_length: float):
        """Create new PercentMAC object using Index object.

        Args:
            idx (Index): Index object
            lemac_at (float): Horizontal distance in length units
            from the station zero to location of the Leading Edge of the MAC / RC
            macrc_length (float): Length of
            Mean Aerodynamic Chord / Reference Chord in length units

        Returns:
            PercentMAC: PercentMAC object derived from Index object
        """
        return PercentMAC(
            ((idx.moment / idx.weight) + idx.ref_st - lemac_at) / (macrc_length / 100),
            lemac_at,
            macrc_length,
        )

    def to_idx(self, weight: int, ref_st: float, c: int, k: int):
        """Convert PercentMAC object to Index object.

        Args:
            weight (int): Corresponding weight
            ref_st (float): Reference station/axis. Selected station
            around which all index values are calculated
            c (int): Constant used as a denominator to convert
            moment values into index values
            k (int): Constant used as a plus value to avoid
            negative index figures

        Raises:
            NotImplementedError: _description_
        """
        # TODO: implement this!
        raise NotImplementedError(
            "Conversion from PercentMAC to Index is not yet implemented"
        )
