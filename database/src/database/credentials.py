"""Approved at-rest treatment for every classified credential field.

Resolves the required treatment from Model's own credential classification
(``CredentialTreatment``): a one-way hash for verification-only credentials,
authenticated reversible protection for recoverable secrets. A field whose
declared treatment is missing or unsupported is rejected rather than
persisted unprotected. Any transformation key comes from Database's private
runtime secret source (the runtime environment) and is never committed.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import os

from cryptography.fernet import Fernet, InvalidToken
from model import CredentialTreatment

_HASH_ALGORITHM = "sha256"
_HASH_ITERATIONS = 390_000
_ENCRYPTION_KEY_ENV_VAR = "DATABASE_CREDENTIAL_ENCRYPTION_KEY"


class UnsupportedCredentialTreatmentError(ValueError):
    """Raised when a credential's declared at-rest treatment is missing or unsupported."""


class MissingEncryptionKeyError(RuntimeError):
    """Raised when an encrypted credential operation is attempted without a configured key."""


class CredentialDecryptionError(ValueError):
    """Raised when a stored encrypted credential cannot be decrypted with the configured key."""


def _encryption_key() -> bytes:
    raw = os.environ.get(_ENCRYPTION_KEY_ENV_VAR)
    if not raw:
        msg = (
            f"{_ENCRYPTION_KEY_ENV_VAR} is not set; required to persist or read an encrypted credential. "
            "Generate one with: python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'"
        )
        raise MissingEncryptionKeyError(msg)
    return raw.encode("utf-8")


def hash_value(plaintext: str) -> str:
    """Apply the one-way hash at-rest treatment; the result cannot be reversed to the original value."""
    salt = os.urandom(16)
    derived = hashlib.pbkdf2_hmac(
        _HASH_ALGORITHM, plaintext.encode("utf-8"), salt, _HASH_ITERATIONS
    )
    return f"pbkdf2_sha256${_HASH_ITERATIONS}${base64.b64encode(salt).decode()}${base64.b64encode(derived).decode()}"


def verify_hash(plaintext: str, stored: str) -> bool:
    """Verify a plaintext value against a hash-treated stored value without ever reversing it."""
    try:
        _algorithm, iterations, salt_b64, derived_b64 = stored.split("$")
    except ValueError:
        return False
    salt = base64.b64decode(salt_b64)
    expected = base64.b64decode(derived_b64)
    candidate = hashlib.pbkdf2_hmac(
        _HASH_ALGORITHM, plaintext.encode("utf-8"), salt, int(iterations)
    )
    return hmac.compare_digest(candidate, expected)


def encrypt_value(plaintext: str) -> str:
    """Apply the authenticated, reversible at-rest treatment."""
    return Fernet(_encryption_key()).encrypt(plaintext.encode("utf-8")).decode("utf-8")


def decrypt_value(token: str) -> str:
    """Recover the original value from an encryption-treated stored value using the configured key."""
    try:
        return Fernet(_encryption_key()).decrypt(token.encode("utf-8")).decode("utf-8")
    except InvalidToken as exc:
        msg = "Stored credential could not be decrypted with the configured key."
        raise CredentialDecryptionError(msg) from exc


def apply_at_rest_treatment(treatment: str, plaintext: str) -> str:
    """Apply the declared at-rest treatment, rejecting a missing or unsupported one rather than storing it unprotected."""
    if treatment == CredentialTreatment.HASH.value:
        return hash_value(plaintext)
    if treatment == CredentialTreatment.ENCRYPTED.value:
        return encrypt_value(plaintext)
    msg = f"Unsupported credential at-rest treatment: {treatment!r}"
    raise UnsupportedCredentialTreatmentError(msg)
