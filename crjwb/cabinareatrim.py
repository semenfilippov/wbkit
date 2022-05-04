from crjwb.inputclasses import StandardWeights


def calc_pax_influence(
    weights: StandardWeights,
    a_influence: float,
    b_influence: float,
    c_influence: float,
    d_influence: float,
    a_pax: int,
    b_pax: int,
    c_pax: int,
    d_pax: int,
) -> float:
    """
    Calculates PAX index influence.

    Args:
        ``avg_adult_weight`` (int): average adult passenger weight (kg)
        ``a_influence`` (float): cabin section A index influence
        ``b_influence`` (float): cabin section B index influence
        ``c_influence`` (float): cabin section C index influence
        ``d_influence`` (float): cabin section D index influence
        ``a_pax`` (int): number of PAX (adults + children) in cabin section A
        ``b_pax`` (int): number of PAX (adults + children) in cabin section B
        ``c_pax`` (int): number of PAX (adults + children) in cabin section C
        ``d_pax`` (int): number of PAX (adults + children) in cabin section D

    Returns:
        ``float``: PAX index influence
    """
    return weights.adult * (
        a_pax * a_influence
        + b_pax * b_influence
        + c_pax * c_influence
        + d_pax * d_influence
    )


def calc_pax_weight(
    weights: StandardWeights,
    num_adults: int,
    num_children: int,
    num_infants: int,
    cabin_baggage: int,
) -> int:
    """
    Calculates passenger + cabin baggage weight.

    Args:
        avg_adult_weight (int): average adult weight (kg)
        avg_child_weight (int): average child weight (kg)
        avg_infant_weight (int): average infant weight (kg)
        num_adults (int): number of adults
        num_children (int): number of children
        num_infants (int): number of infants
        cabin_baggage (int): cabin baggage weight (kg)

    Returns:
        int: passenger + cabin baggage weight
    """
    return (
        weights.adult * num_adults
        + weights.child * num_children
        + weights.infant * num_infants
        + cabin_baggage
    )
