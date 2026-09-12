"""Credential classification and at-rest transformation.

Every field a persistent Model declares through its ``credential_fields``
class attribute is classified into one of two at-rest treatments before it is
stored, per Database Preferences ``data_logic.credential_storage``:

- ``hash``      — a one-way PBKDF2-HMAC-SHA256 transformation for a credential
                  used only for verification (for example ``password``).
- ``encrypted`` — authenticated encryption (Fernet) for a credential that must
                  be recoverable (for example ``api_key``), keyed from
                  Database's private runtime secret.

Neither transformation is reversed by a generic read: see ``operations.py``
for how a stored representation is withheld from callers.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import os
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken

_PACKAGE_ROOT = Path(__file__).resolve().parent.parent.parent
_SECRETS_DIR = _PACKAGE_ROOT / ".secrets"
_KEY_PATH = _SECRETS_DIR / "encryption.key"

_FIELD_DEFAULTS = {
    "password": "hash",
    "api_key": "encrypted",
}
_FALLBACK_MODE = "encrypted"

_HASH_ITERATIONS = 260_000
_HASH_ALGORITHM = "sha256"


def credential_mode(field_name: str) -> str:
    """Resolve the at-rest treatment for a declared credential field name."""
    return _FIELD_DEFAULTS.get(field_name, _FALLBACK_MODE)


def _load_or_create_key() -> bytes:
    _SECRETS_DIR.mkdir(parents=True, exist_ok=True)
    if _KEY_PATH.exists():
        return _KEY_PATH.read_bytes()
    key = Fernet.generate_key()
    _KEY_PATH.write_bytes(key)
    try:
        os.chmod(_KEY_PATH, 0o600)
    except OSError:  # pragma: no cover - platform without POSIX permissions
        pass
    return key


def _fernet() -> Fernet:
    return Fernet(_load_or_create_key())


def hash_value(plaintext: str) -> str:
    """One-way PBKDF2-HMAC-SHA256 transformation. Never reversible."""
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac(_HASH_ALGORITHM, plaintext.encode("utf-8"), salt, _HASH_ITERATIONS)
    salt_b64 = base64.b64encode(salt).decode()
    digest_b64 = base64.b64encode(digest).decode()
    return f"pbkdf2_sha256${_HASH_ITERATIONS}${salt_b64}${digest_b64}"


def verify_hash(plaintext: str, stored: str) -> bool:
    """Verify a plaintext value against a previously hashed storage representation."""
    try:
        algorithm, iterations, salt_b64, digest_b64 = stored.split("$")
    except ValueError:
        return False
    if algorithm != "pbkdf2_sha256":
        return False
    salt = base64.b64decode(salt_b64)
    expected = base64.b64decode(digest_b64)
    candidate = hashlib.pbkdf2_hmac(
        _HASH_ALGORITHM, plaintext.encode("utf-8"), salt, int(iterations)
    )
    return hmac.compare_digest(candidate, expected)


def encrypt_value(plaintext: str) -> str:
    """Authenticated, reversible encryption keyed from Database's private runtime secret."""
    return _fernet().encrypt(plaintext.encode("utf-8")).decode("ascii")


def decrypt_value(stored: str) -> str:
    """Reverse :func:`encrypt_value`. Raises ``ValueError`` for a tampered or foreign value."""
    try:
        return _fernet().decrypt(stored.encode("ascii")).decode("utf-8")
    except InvalidToken as error:
        raise ValueError("stored value cannot be decrypted with the current key") from error


def transform_for_storage(field_name: str, plaintext: str) -> str:
    """Apply the resolved at-rest transformation for a declared credential field."""
    mode = credential_mode(field_name)
    if mode == "hash":
        return hash_value(plaintext)
    if mode == "encrypted":
        return encrypt_value(plaintext)
    raise ValueError(f"unsupported credential storage mode: {mode!r}")  # pragma: no cover
