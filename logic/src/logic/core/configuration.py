"""Logic's runtime configuration contract and its validation.

Logic owns the contract below and validates each value before the Behaviour that needs it runs.
It never owns the values or their delivery: the environment supplies them, and no value is
stored in source, configuration, messages, or outcomes.

Required runtime values:
    LOGIC_ENCRYPTION_KEY: Secret key, 32 url-safe base64-encoded bytes, that protects the
        encrypted credential Fields of Instance and Account.
"""

import os

from cryptography.fernet import Fernet

ENCRYPTION_KEY = "LOGIC_ENCRYPTION_KEY"


def encryption_cipher() -> Fernet:
    """Return the cipher built from the required encryption key.

    Returns:
        (Fernet): Cipher for the encrypted credential Fields.

    Raises:
        ValueError: When the runtime value is missing or invalid; the message names the value
            and never contains it.
    """
    value = os.environ.get(ENCRYPTION_KEY)
    if not value:
        raise ValueError(f"Required runtime value {ENCRYPTION_KEY} is missing")
    try:
        return Fernet(value)
    except ValueError:
        raise ValueError(
            f"Required runtime value {ENCRYPTION_KEY} is invalid: "
            "expected 32 url-safe base64-encoded bytes"
        ) from None
