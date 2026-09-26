"""At-rest protection of the credential Fields that Model classifies as hashed or encrypted."""

import base64
import hashlib
import hmac
import secrets
from functools import cached_property
from typing import Any

from cryptography.fernet import Fernet
from my_model.interface import AtRest, Sensitivity
from sqlmodel import SQLModel

from my_database.configuration import Configuration

_SCHEME = "scrypt"
_COST = (2**14, 8, 1)  # scrypt N, r, p
_TOKEN_VERSION = 0x80  # first byte of every encrypted stored form
_TOKEN_MINIMUM = 73  # version, timestamp, IV, one block, and signature


def hash_credential(value: str) -> str:
    """Turn a credential value into a salted one-way stored form.

    Args:
        value (str): Plain credential value.

    Returns:
        (str): Stored form holding the parameters, salt, and digest; the value cannot be recovered from it.
    """
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(
        value.encode(), salt=salt, n=_COST[0], r=_COST[1], p=_COST[2]
    )
    return "$".join(
        [
            _SCHEME,
            *map(str, _COST),
            base64.b64encode(salt).decode(),
            base64.b64encode(digest).decode(),
        ]
    )


def is_hashed(value: str) -> bool:
    """Tell whether a value already is a stored form produced by hash_credential.

    Args:
        value (str): Value to inspect.

    Returns:
        (bool): True when the value has the stored-form structure.
    """
    parts = value.split("$")
    return (
        len(parts) == 6
        and parts[0] == _SCHEME
        and all(part.isdigit() for part in parts[1:4])
    )


def check_credential(value: str, stored: str) -> bool:
    """Check a plain credential value against its one-way stored form.

    Args:
        value (str): Plain credential value.
        stored (str): Stored form produced by hash_credential.

    Returns:
        (bool): True when the value produced the stored form.
    """
    _, n, r, p, salt, digest = stored.split("$")
    candidate = hashlib.scrypt(
        value.encode(), salt=base64.b64decode(salt), n=int(n), r=int(r), p=int(p)
    )
    return hmac.compare_digest(candidate, base64.b64decode(digest))


class Protection:
    """Protects and recovers credential values with the secret that the Database Configuration references.

    Attributes:
        configuration (Configuration): The Database Configuration whose Settings reference the encryption secret.
    """

    def __init__(self, configuration: Configuration):
        """Prepare protection over a Database Configuration.

        Args:
            configuration (Configuration): Database Configuration whose Settings reference the encryption secret.
        """
        self.configuration = configuration

    @cached_property
    def _cipher(self) -> Fernet:
        return Fernet(self.configuration.secret("encryption_key"))

    def encrypt(self, value: str) -> str:
        """Turn a credential value into an encrypted stored form.

        Args:
            value (str): Plain credential value.

        Returns:
            (str): Encrypted stored form.
        """
        return self._cipher.encrypt(value.encode()).decode()

    def decrypt(self, stored: str) -> str:
        """Recover the original credential value from its encrypted stored form.

        Args:
            stored (str): Encrypted stored form produced by encrypt.

        Returns:
            (str): The original credential value.
        """
        return self._cipher.decrypt(stored.encode()).decode()

    def is_encrypted(self, value: str) -> bool:
        """Tell whether a value already has the stored form of an encrypted credential.

        The form is recognised by its structure, so a value encrypted under a replaced secret is still recognised and is never encrypted twice.

        Args:
            value (str): Value to inspect.

        Returns:
            (bool): True when the value has the structure of an encrypted stored form.
        """
        try:
            token = base64.urlsafe_b64decode(value.encode())
        except ValueError:
            return False
        return len(token) >= _TOKEN_MINIMUM and token[0] == _TOKEN_VERSION

    def protect(self, entity: type[SQLModel], values: dict[str, Any]) -> dict[str, Any]:
        """Return Field values with every protected credential in the protection its Declaration names.

        Args:
            entity (type[SQLModel]): Entity class whose Declaration classifies the credential Fields.
            values (dict[str, Any]): Field values; a value that already is a stored form is kept as it is.

        Returns:
            (dict[str, Any]): The values with each supplied credential in its protected form.
        """
        protected = dict(values)
        for field in entity.declaration.fields:  # type: ignore[attr-defined]  # every Entity declares its meaning
            if (
                field.sensitivity is not Sensitivity.CREDENTIAL
                or protected.get(field.name) is None
            ):
                continue
            value = protected[field.name]
            if field.at_rest is AtRest.HASH and not is_hashed(value):
                protected[field.name] = hash_credential(value)
            elif field.at_rest is AtRest.ENCRYPTED and not self.is_encrypted(value):
                protected[field.name] = self.encrypt(value)
        return protected
