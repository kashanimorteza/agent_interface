"""At-rest credential transformations.

Database applies the storage mode a field's owning Model already resolved
(``credential`` / ``storage_at_rest`` in the field's JSON schema); it never
re-decides the transformation itself.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import os

from cryptography.fernet import Fernet, InvalidToken

_PBKDF2_ITERATIONS = 600_000
_HASH_PREFIX = "pbkdf2_sha256"


def hash_value(plain: str) -> str:
    """One-way transform for a "hash" mode credential. Never reversible."""
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", plain.encode("utf-8"), salt, _PBKDF2_ITERATIONS
    )
    return f"{_HASH_PREFIX}${_PBKDF2_ITERATIONS}${base64.b64encode(salt).decode('ascii')}${base64.b64encode(digest).decode('ascii')}"


def verify_hash(plain: str, stored: str) -> bool:
    """Verify a plain value against a value produced by hash_value()."""
    try:
        prefix, iterations_str, salt_b64, digest_b64 = stored.split("$")
    except ValueError:
        return False
    if prefix != _HASH_PREFIX:
        return False
    salt = base64.b64decode(salt_b64)
    expected = base64.b64decode(digest_b64)
    actual = hashlib.pbkdf2_hmac(
        "sha256", plain.encode("utf-8"), salt, int(iterations_str)
    )
    return hmac.compare_digest(actual, expected)


def encrypt_value(plain: str, key: bytes) -> str:
    """Reversible transform for an "encrypted" mode credential."""
    return Fernet(key).encrypt(plain.encode("utf-8")).decode("ascii")


def decrypt_value(token: str, key: bytes) -> str:
    """Reverse encrypt_value(). Raises ValueError for an invalid or tampered token."""
    try:
        return Fernet(key).decrypt(token.encode("ascii")).decode("utf-8")
    except InvalidToken as exc:
        raise ValueError(
            "Credential token is invalid or was encrypted with a different key."
        ) from exc
