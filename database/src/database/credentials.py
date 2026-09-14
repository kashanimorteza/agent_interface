"""Credential at-rest protection: the resolved transformation applied to a credential field.

Resolution order (Database Preferences): an explicit Target-stated storage mode for a field
takes precedence; otherwise the field's exact-name default applies; otherwise the selected
fallback mode applies. This module never exposes a recoverable plaintext value except
through `decrypt_value`, which only the party holding the resolved secret key can use.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import os
import secrets as _secrets
from typing import Literal

from cryptography.fernet import Fernet

from .paths import component_root

CredentialMode = Literal["hash", "encrypted"]

_EXPLICIT_MODES: dict[tuple[str, str], CredentialMode] = {
    ("User", "password"): "hash",
    ("User", "api_key"): "hash",
    ("Instance", "password"): "encrypted",
    ("Instance", "api_key"): "encrypted",
    ("Account", "password"): "encrypted",
}
_FIELD_DEFAULTS: dict[str, CredentialMode] = {"password": "hash", "api_key": "encrypted"}
_FALLBACK_MODE: CredentialMode = "encrypted"

_PBKDF2_ITERATIONS = 200_000


def resolve_mode(model_name: str, field_name: str) -> CredentialMode:
    """Resolve the at-rest treatment for one credential field of one Domain Definition."""
    explicit = _EXPLICIT_MODES.get((model_name, field_name))
    if explicit is not None:
        return explicit
    return _FIELD_DEFAULTS.get(field_name, _FALLBACK_MODE)


def _encryption_key(instance: str) -> bytes:
    env_name = f"TRADING_ASSISTANT_{instance.upper()}_DATABASE_ENCRYPTION_KEY"
    from_env = os.environ.get(env_name)
    if from_env:
        return from_env.encode("utf-8")

    secrets_dir = component_root() / ".secrets"
    secrets_dir.mkdir(parents=True, exist_ok=True)
    key_file = secrets_dir / f"{instance}.key"
    if key_file.exists():
        return key_file.read_bytes()

    key = Fernet.generate_key()
    key_file.write_bytes(key)
    key_file.chmod(0o600)
    return key


def hash_value(value: str) -> str:
    """Apply a one-way, irreversible transformation to a verification-only credential."""
    salt = _secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", value.encode("utf-8"), salt, _PBKDF2_ITERATIONS)
    return (
        f"pbkdf2$sha256${_PBKDF2_ITERATIONS}$"
        f"{base64.b64encode(salt).decode()}${base64.b64encode(digest).decode()}"
    )


def verify_hash(value: str, stored: str) -> bool:
    """Verify a candidate value against a value previously transformed by `hash_value`."""
    try:
        _algo, hash_name, iterations_s, salt_b64, digest_b64 = stored.split("$")
    except ValueError:
        return False
    iterations = int(iterations_s)
    salt = base64.b64decode(salt_b64)
    expected = base64.b64decode(digest_b64)
    candidate = hashlib.pbkdf2_hmac(hash_name, value.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(candidate, expected)


def encrypt_value(value: str, *, instance: str) -> str:
    """Apply authenticated, reversible protection to a recoverable credential."""
    return Fernet(_encryption_key(instance)).encrypt(value.encode("utf-8")).decode("utf-8")


def decrypt_value(token: str, *, instance: str) -> str:
    """Recover the plaintext value of a credential protected by `encrypt_value`."""
    return Fernet(_encryption_key(instance)).decrypt(token.encode("utf-8")).decode("utf-8")


def protect(value: str, *, model_name: str, field_name: str, instance: str) -> str:
    """Resolve and apply the at-rest treatment for one credential field's value."""
    mode = resolve_mode(model_name, field_name)
    if mode == "hash":
        return hash_value(value)
    return encrypt_value(value, instance=instance)
