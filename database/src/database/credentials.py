"""Generate and protect the credentials that the Initial Data needs.

This module supports Initial Data preparation only. Database Operations store whatever value they receive,
and Logic applies the same protection to credentials it creates or checks later.

Protection schemes:
    User credentials are stored as a salted one-way hash, `scrypt$<n>$<r>$<p>$<salt>$<digest>` with the salt and
    digest in base64. Instance and Account credentials are stored as a Fernet token, and the encryption key
    lives in the secrets directory, never with the data.
"""

import base64
import hashlib
import hmac
import os
import secrets
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml
from cryptography.fernet import Fernet

CREDENTIAL_BYTES = 32
SCRYPT_COST = {"n": 2**14, "r": 8, "p": 1}
KEY_FILE = "encryption.key"
DELIVERY_FILE = "initial_credentials.yaml"


def generate() -> str:
    """Return a fresh, unpredictable credential from the operating system's secure source.

    Returns:
        (str): URL-safe text carrying 256 bits of randomness.
    """
    return secrets.token_urlsafe(CREDENTIAL_BYTES)


def _digest(secret: str, salt: bytes, n: int, r: int, p: int) -> bytes:
    return hashlib.scrypt(secret.encode(), salt=salt, n=n, r=r, p=p, dklen=32)


def hash_secret(secret: str) -> str:
    """Return the one-way stored form of a credential.

    Args:
        secret (str): Credential to protect.

    Returns:
        (str): Salted hash from which the credential cannot be recovered.
    """
    salt = os.urandom(16)
    cost = SCRYPT_COST
    parts = [
        "scrypt",
        str(cost["n"]),
        str(cost["r"]),
        str(cost["p"]),
        base64.b64encode(salt).decode(),
        base64.b64encode(_digest(secret, salt, **cost)).decode(),
    ]
    return "$".join(parts)


def verify_secret(secret: str, stored: str) -> bool:
    """Check a credential against its stored hash.

    Args:
        secret (str): Credential presented.
        stored (str): Stored form produced by `hash_secret`.

    Returns:
        (bool): True when the credential matches.
    """
    scheme, n, r, p, salt, digest = stored.split("$")
    if scheme != "scrypt":
        return False
    candidate = _digest(secret, base64.b64decode(salt), int(n), int(r), int(p))
    return hmac.compare_digest(candidate, base64.b64decode(digest))


def _private_directory(directory: Path) -> Path:
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    directory.chmod(0o700)
    return directory


def _write_private(path: Path, content: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(descriptor, "wb") as file:
        os.fchmod(file.fileno(), 0o600)
        file.write(content)


def load_or_create_key(directory: Path) -> bytes:
    """Return the encryption key, creating it in an owner-only directory when absent.

    Args:
        directory (Path): Secrets directory that holds the key.

    Returns:
        (bytes): Fernet encryption key.
    """
    path = _private_directory(directory) / KEY_FILE
    if not path.exists():
        _write_private(path, Fernet.generate_key())
    return path.read_bytes()


def encrypt(secret: str, key: bytes) -> str:
    """Return the reversible stored form of a credential.

    Args:
        secret (str): Credential to protect.
        key (bytes): Encryption key.

    Returns:
        (str): Authenticated encrypted token.
    """
    return Fernet(key).encrypt(secret.encode()).decode()


def decrypt(token: str, key: bytes) -> str:
    """Recover a credential from its encrypted form.

    Args:
        token (str): Stored form produced by `encrypt`.
        key (bytes): Encryption key that protected it.

    Returns:
        (str): The original credential.
    """
    return Fernet(key).decrypt(token.encode()).decode()


def deliver(credentials: Mapping[str, Mapping[str, Any]], directory: Path) -> Path:
    """Make the plaintext credentials available to the Human, without logging or printing them.

    Args:
        credentials (Mapping[str, Mapping[str, Any]]): Credentials grouped by the record they belong to.
        directory (Path): Secrets directory, outside version control.

    Returns:
        (Path): Owner-only file that holds the credentials.
    """
    path = _private_directory(directory) / DELIVERY_FILE
    _write_private(path, yaml.safe_dump(dict(credentials), sort_keys=False).encode())
    return path
