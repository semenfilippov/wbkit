from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class IndexConstants:
    """Dataclass for Index constants.

    Args:
        ref_st (float): Reference station/axis. Selected station \
around which all index values are calculated
        c (int): Constant used as a denominator to convert \
moment values into index values
        k (int): Constant used as a plus value to avoid \
negative index figures

    Raises:
        ValueError: if not C > 0
        ValueError: if K < 0
    """

    ref_st: float
    c: int
    k: int

    def __post_init__(self):
        if not self.c > 0:
            raise ValueError("C constant should be greater than 0")
        if self.k < 0:
            raise ValueError("K constant should not be negative")


class Index:
    """Moment index representation."""

    def __init__(self, idx: float, weight: int, rck: IndexConstants) -> None:
        """Create new Index object.

        Args:
            idx (float): Index value
            weight (int): Corresponding weight
            rck (IndexConstants): IndexConstants object
        """
        if weight < 0:
            raise ValueError("weight should not be negative")
        self.value = idx
        self.weight = weight
        self.rck = rck

    @staticmethod
    def from_moment(moment: float, weight: int, rck: IndexConstants):
        return Index(moment / rck.c + rck.k, weight, rck)

    @property
    def moment(self) -> float:
        """Get moment value.

        Returns:
            float: moment
        """
        return (self.value - self.rck.k) * self.rck.c

    @staticmethod
    def calc(weight: int, station: float, rck: IndexConstants):
        """Calculate index value and return Index object.

        Args:
            weight (int): Actual weight
            station (float): Horizontal distance in length units
            from station zero to the location
            rck (IndexConstants): IndexConstants object

        Raises:
            ValueError: if `c` equals to zero

        Returns:
            Index: calculated Index object
        """
        try:
            idx = (weight * (station - rck.ref_st)) / rck.c + rck.k
        except ZeroDivisionError:
            raise ValueError("C constant cannot be equal to 0")
        return Index(idx, weight, rck)

    def __validate_calc_ops__(self, other):
        """Internal Index object validator.
        Validate if two Index objects can be added or substracted.
        It is only possible when their `rck` attributes are equal.

        Args:
            other (Index): Index object

        Raises:
            ValueError: if rck attributes are not equal
        """
        if self.rck == other.rck:
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
        if not self.rck.ref_st == other.rck.ref_st:
            raise ValueError(
                "Cannot compare Index instances with different reference stations."
            )

    def __add__(self, other):
        self.__validate_calc_ops__(other)
        sum_weights = self.weight + other.weight
        sum_idxs = self.value + other.value
        return Index(sum_idxs, sum_weights, self.rck)

    def __sub__(self, other):
        self.__validate_calc_ops__(other)
        sum_weights = self.weight - other.weight
        sum_idxs = self.value - other.value
        return Index(sum_idxs, sum_weights, self.rck)

    def __mul__(self, other):
        return Index(self.value * other, self.weight * other, self.rck)

    def __eq__(self, other) -> bool:
        self.__validate_compare_ops__(other)
        return self.moment == other.moment

    def __gt__(self, other) -> bool:
        self.__validate_compare_ops__(other)
        return self.moment > other.moment

    def __lt__(self, other) -> bool:
        self.__validate_compare_ops__(other)
        return self.moment < other.moment

    def __ge__(self, other) -> bool:
        self.__validate_compare_ops__(other)
        return self > other or self == other

    def __le__(self, other) -> bool:
        self.__validate_compare_ops__(other)
        return self < other or self == other


class IndexInfluence:
    """Index influence representation. Basically a convinience class."""

    def __init__(self, influence: float, rck: IndexConstants) -> None:
        """Create new IndexInfluence object.

        Args:
            influence (float): index influence per 1 weight unit
            rck (IndexConstants): IndexConstants object
        """
        self.__influence__ = Index(influence, 1, rck)

    def __mul__(self, other) -> Index:
        return self.__influence__ * other

    def get_idx(self, for_weight: int) -> Index:
        """Get Index object for given weight.

        Args:
            for_weight (int): corresponding weight

        Returns:
            Index: influence multiplied by weight
        """
        return self * for_weight


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
            ((idx.moment / idx.weight) + idx.rck.ref_st - lemac_at)
            / (macrc_length / 100),
            lemac_at,
            macrc_length,
        )

    def to_idx(self, weight: int, rck: IndexConstants):
        """Convert PercentMAC object to Index object.

        Args:
            weight (int): Corresponding weight
            rck (IndexConstants): IndexConstants object

        Returns:
            Index: calculated Index object
        """
        moment = (
            (self.value * (self.macrc_length / 100)) - rck.ref_st + self.lemac_at
        ) * weight
        return Index.from_moment(moment, weight, rck)
