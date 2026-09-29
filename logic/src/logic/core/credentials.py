"""Protection of credential values before they reach Database."""

import base64
import hashlib
import hmac
import os
from enum import StrEnum

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from logic.core.configuration import Configuration

WITHHELD = "********"
_HASHED = "scrypt"
_ENCRYPTED = "fernet"
_COST, _BLOCK, _PARALLEL, _LENGTH, _SALT = 2**14, 8, 1, 32, 16


class Treatment(StrEnum):
    """How a credential Field is stored at rest."""

    HASH = "hash"
    ENCRYPTED = "encrypted"


class CredentialProtector:
    """Turn credential values into their stored form and, where reversible, back."""

    def __init__(self, configuration: Configuration) -> None:
        """Derive the encryption key from the configured secret.

        Args:
            configuration (Configuration): Validated runtime configuration.
        """
        key = HKDF(hashes.SHA256(), 32, None, b"logic-credential-encryption").derive(
            configuration.credential_secret.encode()
        )
        self._cipher = Fernet(base64.urlsafe_b64encode(key))

    def protect(self, treatment: Treatment, value: str) -> str:
        """Return the stored form of a credential value under a treatment."""
        return self.hash(value) if treatment is Treatment.HASH else self.encrypt(value)

    def hash(self, value: str) -> str:
        """Return a one-way stored form from which the value cannot be recovered."""
        salt = os.urandom(_SALT)
        return f"{_HASHED}${salt.hex()}${_digest(value, salt).hex()}"

    def verify(self, candidate: str, stored: str) -> bool:
        """Report whether a candidate equals the value a one-way stored form protects."""
        kind, _, rest = stored.partition("$")
        salt, _, digest = rest.partition("$")
        if kind != _HASHED or not salt or not digest:
            return False
        return hmac.compare_digest(
            _digest(candidate, bytes.fromhex(salt)).hex(), digest
        )

    def encrypt(self, value: str) -> str:
        """Return a reversible stored form that only the configured secret opens."""
        return f"{_ENCRYPTED}${self._cipher.encrypt(value.encode()).decode()}"

    def recover(self, stored: str) -> str | None:
        """Return the original of an encrypted stored form, or None when it is not one this secret opens."""
        kind, _, token = stored.partition("$")
        if kind != _ENCRYPTED:
            return None
        try:
            return self._cipher.decrypt(token.encode()).decode()
        except InvalidToken:
            return None


def _digest(value: str, salt: bytes) -> bytes:
    return hashlib.scrypt(
        value.encode(), salt=salt, n=_COST, r=_BLOCK, p=_PARALLEL, dklen=_LENGTH
    )
