"""At-rest transformations for credential fields.

``hash`` is a one-way, salted, memory-hard transformation that can be
verified but never recovered. ``encrypted`` is a reversible transformation
whose key is read from the runtime environment and never from a package or
generated file. ``plaintext`` stores the value as given.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import secrets

from cryptography.fernet import Fernet, InvalidToken

from ..errors import ConfigurationError, InvalidOperation

HASH_PREFIX = "scrypt"
ENCRYPTED_PREFIX = "fernet"
SCRYPT_N, SCRYPT_R, SCRYPT_P = 2**14, 8, 1
SCRYPT_MAXMEM = 64 * 2**20


def generate_encryption_key() -> str:
    """A new key suitable for the reversible at-rest mode."""
    return Fernet.generate_key().decode("ascii")


class CredentialTransformer:
    def __init__(self, encryption_key: str | None, key_name: str) -> None:
        self._key = encryption_key
        self._key_name = key_name

    def _cipher(self) -> Fernet:
        if not self._key:
            raise ConfigurationError(
                f"the reversible at-rest mode needs the secret {self._key_name} "
                f"in the runtime environment"
            )
        try:
            return Fernet(self._key.encode("ascii"))
        except (ValueError, TypeError) as exc:
            raise ConfigurationError(f"{self._key_name} is not a valid encryption key") from exc

    # -- storing -------------------------------------------------------------

    def transform(self, mode: str, value: str) -> str:
        match mode:
            case "plaintext":
                return value
            case "hash":
                salt = secrets.token_bytes(16)
                digest = hashlib.scrypt(
                    value.encode("utf-8"), salt=salt, n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P,
                    maxmem=SCRYPT_MAXMEM,
                )
                return "$".join(
                    (HASH_PREFIX, str(SCRYPT_N), str(SCRYPT_R), str(SCRYPT_P), _b64(salt), _b64(digest))
                )
            case "encrypted":
                token = self._cipher().encrypt(value.encode("utf-8")).decode("ascii")
                return f"{ENCRYPTED_PREFIX}${token}"
        raise InvalidOperation(f"unknown at-rest mode {mode!r}")

    # -- verifying and recovering -------------------------------------------

    def verify(self, mode: str, stored: str, given: str) -> bool:
        match mode:
            case "plaintext":
                return hmac.compare_digest(stored.encode("utf-8"), given.encode("utf-8"))
            case "hash":
                try:
                    prefix, n, r, p, salt, digest = stored.split("$")
                    if prefix != HASH_PREFIX:
                        return False
                    expected = _unb64(digest)
                    actual = hashlib.scrypt(
                        given.encode("utf-8"), salt=_unb64(salt), n=int(n), r=int(r), p=int(p),
                        maxmem=SCRYPT_MAXMEM,
                    )
                except (ValueError, TypeError):
                    return False
                return hmac.compare_digest(expected, actual)
            case "encrypted":
                try:
                    recovered = self.recover(mode, stored)
                except (InvalidOperation, ConfigurationError):
                    return False
                return hmac.compare_digest(recovered.encode("utf-8"), given.encode("utf-8"))
        raise InvalidOperation(f"unknown at-rest mode {mode!r}")

    def recover(self, mode: str, stored: str) -> str:
        if mode == "plaintext":
            return stored
        if mode != "encrypted":
            raise InvalidOperation(f"a credential stored in {mode!r} mode cannot be recovered")
        prefix, _, token = stored.partition("$")
        if prefix != ENCRYPTED_PREFIX or not token:
            raise InvalidOperation("the stored value is not a reversible credential")
        try:
            return self._cipher().decrypt(token.encode("ascii")).decode("utf-8")
        except InvalidToken as exc:
            raise InvalidOperation("the runtime key does not recover this credential") from exc


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii")


def _unb64(text: str) -> bytes:
    return base64.urlsafe_b64decode(text.encode("ascii"))
