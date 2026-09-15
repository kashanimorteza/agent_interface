"""Applies the at-rest treatment declared by a Model's published credential classification.

Database never infers a credential's treatment from a field name; it applies
exactly the classification the Model publishes and rejects anything else.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import os

from cryptography.fernet import Fernet

_HASH_ITERATIONS = 200_000
_CREDENTIAL_KEY_ENV_VAR = "DATABASE_CREDENTIAL_KEY"


class UnsupportedCredentialTreatmentError(Exception):
    """Raised when a credential field's declared classification is missing or unsupported."""


def hash_value(value: str) -> str:
    """One-way transformation for verification-only credentials."""
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", value.encode(), salt, _HASH_ITERATIONS)
    return f"{base64.b64encode(salt).decode()}${base64.b64encode(digest).decode()}"


def verify_hash(value: str, stored: str) -> bool:
    """Verify a candidate value against a previously hashed credential."""
    salt_b64, digest_b64 = stored.split("$", 1)
    salt = base64.b64decode(salt_b64)
    expected = base64.b64decode(digest_b64)
    actual = hashlib.pbkdf2_hmac("sha256", value.encode(), salt, _HASH_ITERATIONS)
    return hmac.compare_digest(actual, expected)


def _credential_key() -> bytes:
    """Resolve the encryption key from Database's private runtime secret source.

    Delivered through Platform's Runtime Binding once Launch is implemented; until
    then this resolves the documented environment variable, and generates an
    ephemeral development-only key when it is unset so the process stays usable
    outside a configured environment.
    """
    key = os.environ.get(_CREDENTIAL_KEY_ENV_VAR)
    if key is None:
        key = Fernet.generate_key().decode()
        os.environ[_CREDENTIAL_KEY_ENV_VAR] = key
    return key.encode()


def encrypt_value(value: str) -> str:
    """Authenticated, reversible protection for recoverable secrets."""
    return Fernet(_credential_key()).encrypt(value.encode()).decode()


def decrypt_value(token: str) -> str:
    """Reverse `encrypt_value` using the same runtime secret source."""
    return Fernet(_credential_key()).decrypt(token.encode()).decode()


_TREATMENTS = {"hash": hash_value, "encrypted": encrypt_value}


def apply_treatment(classification: str | None, value: str) -> str:
    """Apply the declared at-rest treatment; reject a missing or unsupported classification."""
    if classification not in _TREATMENTS:
        raise UnsupportedCredentialTreatmentError(classification)
    return _TREATMENTS[classification](value)
