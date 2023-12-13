def satoshis_to_bitcoin(satoshis: int):
    """
    Convert satoshis to bitcoin.

    Parameters:
    - satoshis (int): The amount in satoshis to be converted.

    Returns:
    - float: The equivalent amount in bitcoin.
    """
    bitcoin = satoshis / 100000000.0
    return bitcoin
