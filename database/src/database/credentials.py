"""Credential at-rest treatment (Database Preferences credential_storage_modes).

Applies the storage mode Model declares for each credential field before it
reaches storage, and never exposes a stored or original credential value
through any public result.
"""

from __future__ import annotations

import base64
import hashlib
import os
import secrets

from cryptography.fernet import Fernet, InvalidToken

from database.exceptions import DatabaseConfigurationError, UnsupportedCredentialModeError

REDACTED = "«redacted»"

_PBKDF2_ALGORITHM = "pbkdf2_sha256"
_PBKDF2_ITERATIONS = 600_000
_ENCRYPTION_KEY_ENV_VAR = "DATABASE_ENCRYPTION_KEY"


def hash_credential(value: str) -> str:
    """One-way transformation for a verification-only credential. Never reversible."""
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", value.encode(), salt, _PBKDF2_ITERATIONS)
    return (
        f"{_PBKDF2_ALGORITHM}${_PBKDF2_ITERATIONS}"
        f"${base64.urlsafe_b64encode(salt).decode()}${base64.urlsafe_b64encode(digest).decode()}"
    )


def verify_hashed_credential(value: str, stored: str) -> bool:
    algorithm, iterations_s, salt_b64, digest_b64 = stored.split("$")
    if algorithm != _PBKDF2_ALGORITHM:
        raise UnsupportedCredentialModeError(f"Unsupported hash algorithm {algorithm!r}")
    salt = base64.urlsafe_b64decode(salt_b64)
    expected = base64.urlsafe_b64decode(digest_b64)
    actual = hashlib.pbkdf2_hmac("sha256", value.encode(), salt, int(iterations_s))
    return secrets.compare_digest(actual, expected)


def _encryption_key() -> bytes:
    raw = os.environ.get(_ENCRYPTION_KEY_ENV_VAR)
    if not raw:
        raise DatabaseConfigurationError(
            f"{_ENCRYPTION_KEY_ENV_VAR} is not set. Generate one with: "
            'python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())" '
            f"and export it as {_ENCRYPTION_KEY_ENV_VAR} before running migrations, imports, or data operations."
        )
    return raw.encode()


def encrypt_credential(value: str) -> str:
    """Authenticated reversible protection for a recoverable credential."""
    return Fernet(_encryption_key()).encrypt(value.encode()).decode()


def decrypt_credential(stored: str) -> str:
    try:
        return Fernet(_encryption_key()).decrypt(stored.encode()).decode()
    except InvalidToken as exc:
        raise DatabaseConfigurationError(
            "Stored credential could not be decrypted with the current encryption key."
        ) from exc


def apply_at_rest_treatment(mode: str, value: str) -> str:
    if mode == "hash":
        return hash_credential(value)
    if mode == "encrypted":
        return encrypt_credential(value)
    raise UnsupportedCredentialModeError(f"Unsupported credential storage mode {mode!r}")
