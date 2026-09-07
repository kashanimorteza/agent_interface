"""At-rest transformations of credential fields.

``hash`` is a salted one-way hash suitable for verification; ``encrypted`` is
reversible encryption under a cipher key derived from the configured secret;
``plaintext`` stores the value unchanged. The stored representation never
leaves the Database boundary.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
from typing import Callable

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from ..errors import CredentialKeyError, OperationError

HASH_SCHEME = "pbkdf2_sha256"
HASH_ITERATIONS = 600_000
_HKDF_INFO = b"my_database credential encryption"
MODES = ("plaintext", "hash", "encrypted")

KeyProvider = Callable[[], str]


def generate_credential() -> str:
    """A cryptographically random credential value (for generate instructions)."""
    return secrets.token_urlsafe(32)


def hash_credential(value: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", value.encode(), salt, HASH_ITERATIONS)
    return "$".join((HASH_SCHEME, str(HASH_ITERATIONS), _b64(salt), _b64(digest)))


def verify_hashed(value: str, stored: str) -> bool:
    try:
        scheme, iterations, salt, digest = stored.split("$")
        if scheme != HASH_SCHEME:
            return False
        candidate = hashlib.pbkdf2_hmac("sha256", value.encode(), _unb64(salt), int(iterations))
        return hmac.compare_digest(candidate, _unb64(digest))
    except (ValueError, TypeError):
        return False


def cipher(secret: str) -> Fernet:
    """The cipher for a secret: any non-empty secret is accepted and a 32-byte
    key is derived from it, so the URL-safe base64 of 32 random bytes is one
    valid value among many."""
    if not secret or not secret.strip():
        raise CredentialKeyError("the credential-encryption key is empty")
    derived = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=_HKDF_INFO).derive(secret.encode())
    return Fernet(base64.urlsafe_b64encode(derived))


def encrypt_credential(value: str, secret: str) -> str:
    return cipher(secret).encrypt(value.encode()).decode()


def decrypt_credential(stored: str, secret: str) -> str:
    try:
        return cipher(secret).decrypt(stored.encode()).decode()
    except InvalidToken:
        raise CredentialKeyError("the stored credential cannot be decrypted with the configured key") from None


def transform(mode: str, value: str, key: KeyProvider) -> str:
    """The stored representation of a credential value under an at-rest mode."""
    if mode == "hash":
        return hash_credential(value)
    if mode == "encrypted":
        return encrypt_credential(value, key())
    if mode == "plaintext":
        return value
    raise OperationError(f"unsupported credential storage mode {mode!r}")


def _b64(raw: bytes) -> str:
    return base64.b64encode(raw).decode()


def _unb64(text: str) -> bytes:
    return base64.b64decode(text.encode())
