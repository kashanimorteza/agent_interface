"""Credential at-rest transformations: one-way hash (scrypt) and reversible encryption (Fernet)."""

from __future__ import annotations

import base64
import hashlib
import hmac
import secrets

from cryptography.fernet import Fernet

from trading_database.errors import CredentialKeyMissingError, UnsupportedCredentialModeError
from trading_database.settings import get_settings

HASH_PREFIX = "scrypt"
_SCRYPT_N, _SCRYPT_R, _SCRYPT_P, _DKLEN, _SALT_BYTES = 2**14, 8, 1, 32, 16
MODES = ("plaintext", "hash", "encrypted")


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _unb64(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def _scrypt(value: str, salt: bytes, n: int, r: int, p: int) -> bytes:
    return hashlib.scrypt(value.encode("utf-8"), salt=salt, n=n, r=r, p=p, dklen=_DKLEN)


def hash_credential(value: str) -> str:
    """Salted one-way hash: ``scrypt$<n>$<r>$<p>$<salt>$<hash>``."""
    salt = secrets.token_bytes(_SALT_BYTES)
    digest = _scrypt(value, salt, _SCRYPT_N, _SCRYPT_R, _SCRYPT_P)
    return f"{HASH_PREFIX}${_SCRYPT_N}${_SCRYPT_R}${_SCRYPT_P}${_b64(salt)}${_b64(digest)}"


def verify_hashed_credential(value: str, stored: str) -> bool:
    """Constant-time check of ``value`` against a stored hash string."""
    try:
        prefix, n, r, p, salt, digest = stored.split("$")
        if prefix != HASH_PREFIX:
            return False
        candidate = _scrypt(value, _unb64(salt), int(n), int(r), int(p))
        return hmac.compare_digest(candidate, _unb64(digest))
    except (ValueError, TypeError):
        return False


def _resolve_key(key: str | None) -> bytes:
    resolved = key if key is not None else get_settings().credential_encryption_key
    if not resolved:
        raise CredentialKeyMissingError(
            "CREDENTIAL_ENCRYPTION_KEY is not configured; it is required to write an encrypted credential"
        )
    return resolved.encode("ascii")


def encrypt_credential(value: str, key: str | None = None) -> str:
    """Reversible encryption with the configured Fernet key."""
    return Fernet(_resolve_key(key)).encrypt(value.encode("utf-8")).decode("ascii")


def decrypt_credential(token: str, key: str | None = None) -> str:
    """Inverse of :func:`encrypt_credential`; internal use only."""
    return Fernet(_resolve_key(key)).decrypt(token.encode("ascii")).decode("utf-8")


def transform_for_storage(value: str, mode: str, key: str | None = None) -> str:
    """Apply the at-rest mode resolved for a credential field."""
    if mode == "plaintext":
        return value
    if mode == "hash":
        return hash_credential(value)
    if mode == "encrypted":
        return encrypt_credential(value, key)
    raise UnsupportedCredentialModeError(f"unsupported credential storage mode: {mode!r}")
