"""Secure generation of credential values."""

import secrets


def generate_credential(nbytes: int = 32) -> str:
    """Generate an unpredictable credential value.

    Args:
        nbytes (int): Number of random bytes of entropy.

    Returns:
        (str): URL-safe text carrying the random bytes.
    """
    return secrets.token_urlsafe(nbytes)
