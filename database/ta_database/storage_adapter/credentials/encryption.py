"""Reversible encryption for credential columns resolved to the ``encrypted`` mode.

The key comes only from runtime settings (``TA_DATABASE_ENCRYPTION_KEY``); there
is no built-in fallback key.
"""

from __future__ import annotations

from cryptography.fernet import Fernet, InvalidToken

from ta_database.settings import ENV_ENCRYPTION_KEY, get_settings


class MissingEncryptionKey(RuntimeError):
    """Raised when an encrypted credential is used without a configured key."""


class InvalidEncryptedValue(ValueError):
    """Raised when a stored value cannot be decrypted with the configured key."""


def _fernet() -> Fernet:
    key = get_settings().encryption_key
    if not key:
        raise MissingEncryptionKey(f"{ENV_ENCRYPTION_KEY} is not set; encrypted credentials cannot be used")
    return Fernet(key.encode("utf-8") if isinstance(key, str) else key)


def encrypt_credential(value: str) -> str:
    return _fernet().encrypt(value.encode("utf-8")).decode("ascii")


def decrypt_credential(token: str) -> str:
    try:
        return _fernet().decrypt(token.encode("ascii")).decode("utf-8")
    except InvalidToken as exc:
        raise InvalidEncryptedValue("stored value is not a valid token for the configured key") from exc
