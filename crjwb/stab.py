def calc_stab(mactow: float, eicas_formatted: bool = False) -> float:
    """
    Get takeoff stab trim setting for given %MAC.

    The function is derived from the fact that:

    MAC 8.8 => STAB 8.15

    MAC 35  => STAB 4.00

    Therefore:

    f(x) = -0.158397x + 9.54389

    Args:
        ``mactow`` (float): %MAC for takeoff
        ``eicas_formatted`` (bool, optional): Whether to round first decimal \
        to even number.
        Defaults to False.

    Raises:
        ``ValueError``: If provided ``mactow`` is out of range (8.8-35.0)

    Returns:
        ``float``: stabilizer trim setting
    """
    if mactow < 8.8 or mactow > 35:
        raise ValueError(
            f"MAC {mactow} is out of range. Should be within 8.8-35.0 %MAC."
        )
    stab = mactow * -0.158397 + 9.54389
    if eicas_formatted:
        return round(stab / 2, 1) * 2
    else:
        return round(stab, 2)
