def calc_stab(mactow: float) -> float:
    """
    Get takeoff stab trim setting for given %MAC.

    The function is derived from the fact that:

    MAC 8.8 => STAB 8.15

    MAC 35  => STAB 4.00

    Therefore:

    f(x) = -0.158397x + 9.54389

    Args:
        ``mactow`` (float): %MAC for takeoff

    Raises:
        ``ValueError``: If provided ``mactow`` is out of range (8.8-35.0)

    Returns:
        ``float``: stabilizer trim setting
    """
    if mactow < 8.8 or mactow > 35:
        raise ValueError(
            f"MAC {mactow} is out of range. Should be within 8.8-35.0 %MAC."
        )
    return mactow * -0.158397 + 9.54389


def eicas_round(stab_trim_setting: float) -> float:
    """
    Rounds stab trim setting up to 0.2 (as displayed on EICAS).

    Args:
        ``stab_trim_setting`` (float): stab trim setting

    Returns:
        ``float``: rounded value
    """
    return round(stab_trim_setting / 2, 1) * 2
