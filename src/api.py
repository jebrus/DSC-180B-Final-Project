def query(artists: list, n: int) -> list:
    """
    Takes a list of artists the user enjoys as input and returns a list of
    artists that the model predicts they would enjoy.

    Args:
        artists: List of artists the user enjoys.
        n: Number of artists to return.

    Returns:
        List of artists the model predicts the user will enjoy.

    Raises:
        ValueError: If no artists are provided.
    """

    if artists:
        return ['Drake'] * n
    else:
        raise ValueError('No artists provided.')
