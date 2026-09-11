"""Database's private runtime secret source and credential at-rest transformations.

Connection credentials and encryption keys never appear in committed files.
The encryption key is read from the runtime environment; when absent (local
development), one is generated and persisted under a git-ignored, package-
private location so it is never distributed or source-controlled.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import os
import secrets
from pathlib import Path

from cryptography.fernet import Fernet

_PACKAGE_ROOT = Path(__file__).resolve().parent.parent.parent
_LOCAL_SECRETS_DIR = _PACKAGE_ROOT / ".secrets"
_LOCAL_KEY_FILE = _LOCAL_SECRETS_DIR / "encryption.key"
_ENV_KEY_NAME = "TRADING_ASSISTANT_DATABASE_ENCRYPTION_KEY"

_HASH_ITERATIONS = 200_000


def _encryption_key() -> bytes:
    from_env = os.environ.get(_ENV_KEY_NAME)
    if from_env:
        return from_env.encode()
    if _LOCAL_KEY_FILE.exists():
        return _LOCAL_KEY_FILE.read_bytes()
    _LOCAL_SECRETS_DIR.mkdir(parents=True, exist_ok=True)
    key = Fernet.generate_key()
    _LOCAL_KEY_FILE.write_bytes(key)
    return key


def generate_secure_value() -> str:
    """A securely generated value for a credential field pending generation."""
    return secrets.token_urlsafe(32)


def hash_value(value: str) -> str:
    """A one-way transformation; the original value cannot be recovered."""
    salt = os.urandom(16)
    derived = hashlib.pbkdf2_hmac("sha256", value.encode(), salt, _HASH_ITERATIONS)
    return f"pbkdf2_sha256${_HASH_ITERATIONS}${base64.b64encode(salt).decode()}${base64.b64encode(derived).decode()}"


def verify_hash(value: str, stored: str) -> bool:
    algo, iterations, salt_b64, derived_b64 = stored.split("$")
    salt = base64.b64decode(salt_b64)
    expected = base64.b64decode(derived_b64)
    candidate = hashlib.pbkdf2_hmac("sha256", value.encode(), salt, int(iterations))
    return hmac.compare_digest(candidate, expected)


def encrypt_value(value: str) -> str:
    """A reversible transformation using Database's private encryption key."""
    return Fernet(_encryption_key()).encrypt(value.encode()).decode()


def decrypt_value(stored: str) -> str:
    return Fernet(_encryption_key()).decrypt(stored.encode()).decode()


def plaintext_value(value: str) -> str:
    return value
