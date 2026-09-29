"""One-way hashing and reversible encryption of credential values."""

import base64
import hashlib
import secrets

from cryptography.fernet import Fernet

_COST = {"n": 2**14, "r": 8, "p": 1}


def _encode(data: bytes) -> str:
    return base64.b64encode(data).decode()


def hash_secret(plain: str) -> str:
    """Hash a credential one way with a fresh random salt.

    Args:
        plain (str): Plaintext credential.

    Returns:
        (str): Self-describing hash from which the plaintext cannot be recovered.
    """
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(plain.encode(), salt=salt, **_COST)
    n, r, p = _COST.values()
    return f"scrypt${n}${r}${p}${_encode(salt)}${_encode(digest)}"


def encrypt_secret(plain: str, key: str) -> str:
    """Encrypt a credential so that only the holder of the key can recover it.

    Args:
        plain (str): Plaintext credential.
        key (str): Protection key.

    Returns:
        (str): Encrypted token.
    """
    return Fernet(key).encrypt(plain.encode()).decode()


def decrypt_secret(token: str, key: str) -> str:
    """Recover a credential encrypted with the same key.

    Args:
        token (str): Encrypted token.
        key (str): Protection key.

    Returns:
        (str): Plaintext credential.
    """
    return Fernet(key).decrypt(token.encode()).decode()
