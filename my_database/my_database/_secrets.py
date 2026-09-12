"""Database's private runtime secret source.

Holds only the local encryption key used for the ``encrypted`` credential
storage mode. Never committed (the containing directory is gitignored),
never exposed through the public interface, and never read by another layer.
"""

from __future__ import annotations

import os
import stat

from cryptography.fernet import Fernet

from my_database._config import SECRETS_DIR

_KEY_FILE = SECRETS_DIR / "encryption.key"
_ENV_VAR = "TRADING_ASSISTANT_GENERAL_DATABASE_ENCRYPTION_KEY"


def _generate_and_store_key() -> bytes:
    SECRETS_DIR.mkdir(parents=True, exist_ok=True)
    key = Fernet.generate_key()
    _KEY_FILE.write_bytes(key)
    os.chmod(_KEY_FILE, stat.S_IRUSR | stat.S_IWUSR)
    return key


def get_encryption_key() -> bytes:
    """Resolve the encryption key: an environment override first, then the
    layer-local secret file, generating it on first use.
    """

    from_env = os.environ.get(_ENV_VAR)
    if from_env:
        return from_env.encode("utf-8")
    if _KEY_FILE.is_file():
        return _KEY_FILE.read_bytes()
    return _generate_and_store_key()
