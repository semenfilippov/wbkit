def calc_stab(mac: float, eicas_formatted: bool = False) -> float:
    """
    Get stab trim setting for given %MAC.\n
    The function is derived from the fact that:\n
    MAC 8.8 => STAB 8.15\n
    MAC 35  => STAB 4.00\n
    Therefore:\n
    f(x) = -0.158397x + 9.54389\n
    Args:
        mac (float): %MAC
        eicas_formatted (bool, optional): Whether to round first decimal to even number.
        Defaults to False.

    Raises:
        ValueError: If provided %MAC is out of bounds (8.8-35.0)

    Returns:
        float: stabilizer trim setting
    """
    if mac < 8.8 or mac > 35:
        raise ValueError(f"MAC {mac} is out of bounds. Should be within 8.8-35.0 %MAC.")
    stab = mac * -0.158397 + 9.54389
    if eicas_formatted:
        return round(stab / 2, 1) * 2
    else:
        return round(stab, 2)
