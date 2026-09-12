"""Applies the persistence transformation a Model-declared credential field
requires, and reverses it only where the declared mode permits recovery.

Database never decides which fields are credentials or which storage mode
they need: it reads that decision from each field's own
``json_schema_extra`` (``credential`` and ``storage_at_rest``), set by the
Model package. An explicit Model-declared mode always wins over any of
Database's own generic field-name defaults.
"""

from __future__ import annotations

import hashlib
import hmac
import os

from cryptography.fernet import Fernet

from my_database._secrets import get_encryption_key

REDACTED = "<redacted>"

_HASH_ITERATIONS = 600_000
_HASH_ALGORITHM = "sha256"


def hash_value(plain: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac(_HASH_ALGORITHM, plain.encode("utf-8"), salt, _HASH_ITERATIONS)
    return f"pbkdf2${_HASH_ALGORITHM}${_HASH_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_hash(plain: str, stored: str) -> bool:
    try:
        _, algorithm, iterations, salt_hex, digest_hex = stored.split("$")
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(digest_hex)
    except (ValueError, AttributeError):
        return False
    candidate = hashlib.pbkdf2_hmac(algorithm, plain.encode("utf-8"), salt, int(iterations))
    return hmac.compare_digest(candidate, expected)


def encrypt_value(plain: str) -> str:
    fernet = Fernet(get_encryption_key())
    return fernet.encrypt(plain.encode("utf-8")).decode("ascii")


def decrypt_value(token: str) -> str:
    fernet = Fernet(get_encryption_key())
    return fernet.decrypt(token.encode("ascii")).decode("utf-8")
