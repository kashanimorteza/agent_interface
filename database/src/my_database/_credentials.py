from __future__ import annotations

import hashlib
import os
import secrets
from pathlib import Path

from cryptography.fernet import Fernet

REDACTED = "**redacted**"

_SECRET_DIR = Path(__file__).resolve().parent.parent.parent / ".secrets"
_KEY_ENV_VAR = "DATABASE_ENCRYPTION_KEY"
_KEY_FILE = _SECRET_DIR / "encryption.key"

_PBKDF2_ITERATIONS = 200_000


def _encryption_key() -> bytes:
    env_value = os.environ.get(_KEY_ENV_VAR)
    if env_value:
        return env_value.encode()
    if _KEY_FILE.exists():
        return _KEY_FILE.read_bytes()
    _SECRET_DIR.mkdir(parents=True, exist_ok=True)
    key = Fernet.generate_key()
    _KEY_FILE.write_bytes(key)
    _KEY_FILE.chmod(0o600)
    return key


def hash_value(value: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", value.encode(), salt, _PBKDF2_ITERATIONS)
    return f"{salt.hex()}:{digest.hex()}"


def verify_hashed(value: str, stored: str) -> bool:
    salt_hex, digest_hex = stored.split(":", 1)
    salt = bytes.fromhex(salt_hex)
    digest = hashlib.pbkdf2_hmac("sha256", value.encode(), salt, _PBKDF2_ITERATIONS)
    return digest.hex() == digest_hex


def encrypt_value(value: str) -> str:
    return Fernet(_encryption_key()).encrypt(value.encode()).decode()


def decrypt_value(token: str) -> str:
    return Fernet(_encryption_key()).decrypt(token.encode()).decode()
