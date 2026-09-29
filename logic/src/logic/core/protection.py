"""At-rest protection of credential values, shared by the Entity Child Services."""

import base64
import hashlib
import hmac
import secrets
from collections.abc import Callable, Mapping
from typing import Any

from cryptography.fernet import InvalidToken

from logic.core.configuration import encryption_cipher

_HASH_PREFIX = "scrypt"
_N, _R, _P = 2**14, 8, 1


def hash_value(plain: str) -> str:
    """Return a salted one-way hash of a value.

    Args:
        plain (str): Value to protect.

    Returns:
        (str): Self-describing hash text; the original value cannot be recovered from it.
    """
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(plain.encode(), salt=salt, n=_N, r=_R, p=_P, dklen=32)
    encoded = [base64.b64encode(part).decode() for part in (salt, digest)]
    return "$".join([_HASH_PREFIX, str(_N), str(_R), str(_P), *encoded])


def encrypt_value(plain: str) -> str:
    """Return a value encrypted with the runtime-supplied key.

    Args:
        plain (str): Value to protect.

    Returns:
        (str): Encrypted text that only the runtime-supplied key can turn back into the value.

    Raises:
        ValueError: When the required runtime value is missing or invalid.
    """
    return encryption_cipher().encrypt(plain.encode()).decode()


def reveal_value(stored: str) -> str:
    """Return the plain value behind an encrypted stored value.

    A stored value that is not encrypted text, such as a seeded credential stored as
    generated, is returned as it is.

    Args:
        stored (str): Stored credential text.

    Returns:
        (str): The plain value.

    Raises:
        ValueError: When the required runtime value is missing or invalid.
    """
    try:
        return encryption_cipher().decrypt(stored.encode()).decode()
    except InvalidToken:
        return stored


def same_value(left: str, right: str) -> bool:
    """Compare two plain values without leaking timing."""
    return hmac.compare_digest(left.encode(), right.encode())


def protect_entity(
    entity: Any,
    treatments: Mapping[str, Callable[[str], str]],
    stored: Any | None = None,
) -> Any:
    """Return the Entity with its credential Fields in protected form.

    A Field with no value stays without a value, and a Field whose value equals the stored
    record's value is already protected and is left unchanged. The given Entity is never
    modified.

    Args:
        entity (Any): Entity instance carrying the supplied values.
        treatments (Mapping[str, Callable[[str], str]]): Protection to apply per Field name.
        stored (Any, optional): The stored record being updated, when there is one.

    Returns:
        (Any): The same Entity when nothing needs protecting, otherwise a new instance of the
            same Entity with the protected values.
    """
    values: dict[str, str] = {}
    for field, protect in treatments.items():
        value = getattr(entity, field)
        if value is None or (stored is not None and getattr(stored, field) == value):
            continue
        values[field] = protect(value)
    if not values:
        return entity
    return type(entity)(**{**entity.model_dump(), **values})
