"""Resolved at-rest treatment for credential Fields (Database Principle 12, Database Preferences
`selected.credential_storage_mode` and `settings.data_logic.credential_storage`).

A Domain Definition's own `CREDENTIAL_STORAGE` (published by Model, Model Principle 2) is the
sole source of which Fields are credentials and which mode applies — this module only implements
the two transformations Database Preferences' `options.credential_storage_modes` declares for
actual credential use: `hash` (one-way, verification only) and `encrypted` (authenticated,
reversible). `plaintext` is not implemented: Database Preferences marks it
`allowed_for_credentials: false`.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import os
import secrets

from cryptography.fernet import Fernet, InvalidToken

from database.errors import DatabaseError

_PBKDF2_ALGORITHM = "sha256"
_PBKDF2_ITERATIONS = 600_000
_HASH_PREFIX = "pbkdf2_sha256"

_ENCRYPTION_KEY_ENV_VAR = "DATABASE_ENCRYPTION_KEY"
"""Database's private runtime secret source (Database Principle 12): a Fernet key delivered
through the runtime environment by Platform, never general configuration or Interface Config
(Database Preferences `options.credential_storage_modes.encrypted.key_source`). This exact
variable name is a Database-owned consequential choice (Database Preferences `settings` state no
name for a credential-encryption key, only for Instance connection secrets), recorded here and in
the README."""


class MissingEncryptionKeyError(DatabaseError):
    """Raised when `encrypted` at-rest treatment is required but no runtime encryption key is
    configured."""


def hash_value(plaintext: str) -> str:
    """Apply the `hash` at-rest treatment: a one-way transformation used only for verification
    (Database Preferences `options.credential_storage_modes.hash`)."""
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        _PBKDF2_ALGORITHM, plaintext.encode("utf-8"), salt, _PBKDF2_ITERATIONS
    )
    return "$".join(
        [
            _HASH_PREFIX,
            str(_PBKDF2_ITERATIONS),
            base64.b64encode(salt).decode("ascii"),
            base64.b64encode(digest).decode("ascii"),
        ]
    )


def verify_hash(plaintext: str, stored: str) -> bool:
    """Verify `plaintext` against a value previously produced by `hash_value`, without ever
    recovering the original plaintext from storage."""
    try:
        algorithm, iterations, salt_b64, digest_b64 = stored.split("$")
    except ValueError:
        return False
    if algorithm != _HASH_PREFIX:
        return False
    salt = base64.b64decode(salt_b64)
    expected = base64.b64decode(digest_b64)
    actual = hashlib.pbkdf2_hmac(
        _PBKDF2_ALGORITHM, plaintext.encode("utf-8"), salt, int(iterations)
    )
    return hmac.compare_digest(actual, expected)


def _resolve_encryption_key() -> bytes:
    raw = os.environ.get(_ENCRYPTION_KEY_ENV_VAR)
    if not raw:
        raise MissingEncryptionKeyError(
            f"Runtime environment variable {_ENCRYPTION_KEY_ENV_VAR} is not set; "
            "`encrypted` at-rest treatment requires Platform to deliver a Fernet key "
            "through the runtime environment (Database Principle 12)."
        )
    return raw.encode("ascii")


def generate_encryption_key() -> str:
    """Generate a new Fernet key suitable for `DATABASE_ENCRYPTION_KEY` (operational tooling,
    not part of the public Database Interface)."""
    return Fernet.generate_key().decode("ascii")


def encrypt_value(plaintext: str) -> str:
    """Apply the `encrypted` at-rest treatment: authenticated, reversible protection
    (Database Preferences `options.credential_storage_modes.encrypted`)."""
    fernet = Fernet(_resolve_encryption_key())
    return fernet.encrypt(plaintext.encode("utf-8")).decode("ascii")


def decrypt_value(token: str) -> str:
    """Recover the original plaintext from a value previously produced by `encrypt_value`.

    Reserved for the capability-restricted controlled-command route (Database Principle 8);
    never called from the standard generic Database Interface read path (Database Principle 12 —
    Database never exposes a credential representation through its public interface)."""
    fernet = Fernet(_resolve_encryption_key())
    try:
        return fernet.decrypt(token.encode("ascii")).decode("utf-8")
    except InvalidToken as exc:
        raise DatabaseError("Stored credential value failed authenticated decryption.") from exc


TRANSFORM_ON_WRITE = {
    "hash": hash_value,
    "encrypted": encrypt_value,
}
"""Dispatch from a Domain Definition's declared credential-storage mode (Model
`CREDENTIAL_STORAGE`, resolved per Database Preferences `settings.data_logic.credential_storage`)
to the transformation applied before a credential Field's value reaches storage."""
