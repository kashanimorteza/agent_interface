"""One-way hashing for credential columns resolved to the ``hash`` mode."""

from __future__ import annotations

import base64
import hashlib
import hmac
import secrets

_PREFIX = "scrypt"
_N, _R, _P, _DKLEN, _SALT_BYTES = 2**14, 8, 1, 32, 16


def _digest(value: str, salt: bytes) -> bytes:
    return hashlib.scrypt(value.encode("utf-8"), salt=salt, n=_N, r=_R, p=_P, dklen=_DKLEN)


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii")


def hash_credential(value: str) -> str:
    """Return ``scrypt$<salt>$<digest>`` with a fresh random salt."""
    salt = secrets.token_bytes(_SALT_BYTES)
    return f"{_PREFIX}${_b64(salt)}${_b64(_digest(value, salt))}"


def verify_credential(value: str, stored: str) -> bool:
    """Return True only when ``value`` produced ``stored``; constant-time compare."""
    if not isinstance(stored, str) or not stored.startswith(_PREFIX + "$"):
        return False
    try:
        _, salt_b64, digest_b64 = stored.split("$", 2)
        salt = base64.urlsafe_b64decode(salt_b64)
        expected = base64.urlsafe_b64decode(digest_b64)
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(_digest(value, salt), expected)
