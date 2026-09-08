"""What happens to a credential between a caller and storage.

Every field the definitions declare as a credential resolves to exactly one
treatment: what the project states wins, then the default for a field of that
name, and only then the layer's general default. The value is transformed on the
way in, and its stored form never travels back out of this layer.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import os
from dataclasses import dataclass
from enum import Enum
from typing import Any

from cryptography.fernet import Fernet, InvalidToken
from my_model import CredentialStorage, Entity, FieldSpec, is_stated

from ..contract import CredentialError
from ..storage_adapter import ENCRYPTION_KEY, require


class AtRest(str, Enum):
    """The supported treatments a credential can be held under."""

    PLAINTEXT = "plaintext"
    HASH = "hash"
    ENCRYPTED = "encrypted"

    @property
    def recoverable(self) -> bool:
        return self is not AtRest.HASH


# Used only when a field is a credential and nothing more specific applies.
GENERAL_DEFAULT = AtRest.PLAINTEXT

# Applied by field name when the definition states no treatment of its own.
BY_FIELD_NAME: dict[str, AtRest] = {
    "password": AtRest.HASH,
    "api_key": AtRest.HASH,
}

_HASH_MARKER = "hash$"
_ENCRYPTED_MARKER = "enc$"
_ITERATIONS = 240_000


@dataclass(frozen=True, slots=True)
class Treatment:
    """The resolved treatment of one credential field."""

    field: str
    mode: AtRest
    stated_by_project: bool

    @property
    def recoverable(self) -> bool:
        return self.mode.recoverable


def resolve(field_name: str, spec: FieldSpec) -> Treatment | None:
    """How this field is held at rest, or ``None`` when it is not a credential.

    A default never turns a field into a credential, and never displaces a
    treatment the project stated.
    """

    if not spec.is_credential():
        return None

    stated = spec.storage_treatment()
    if stated is not None:
        return Treatment(field_name, AtRest(CredentialStorage(stated).value), True)
    if field_name in BY_FIELD_NAME:
        return Treatment(field_name, BY_FIELD_NAME[field_name], False)
    return Treatment(field_name, GENERAL_DEFAULT, False)


def treatments(entity: type[Entity]) -> dict[str, Treatment]:
    """Every credential field of one definition, with its resolved treatment."""

    resolved: dict[str, Treatment] = {}
    for name, spec in entity.entity_fields.items():
        treatment = resolve(name, spec)
        if treatment is not None:
            resolved[name] = treatment
    return resolved


def _key() -> Fernet:
    supplied = require(ENCRYPTION_KEY)
    try:
        return Fernet(supplied.encode())
    except (ValueError, TypeError) as error:
        raise CredentialError(
            f"{ENCRYPTION_KEY} was supplied but is not usable key material"
        ) from error


def protect(value: Any, treatment: Treatment) -> Any:
    """The form a supplied credential is stored in."""

    if value is None:
        return None
    text = str(value)
    if treatment.mode is AtRest.PLAINTEXT:
        return text
    if treatment.mode is AtRest.HASH:
        salt = os.urandom(16)
        digest = hashlib.pbkdf2_hmac("sha256", text.encode(), salt, _ITERATIONS)
        return (
            f"{_HASH_MARKER}{_ITERATIONS}${base64.b64encode(salt).decode()}$"
            f"{base64.b64encode(digest).decode()}"
        )
    return f"{_ENCRYPTED_MARKER}{_key().encrypt(text.encode()).decode()}"


def matches(candidate: str, stored: Any, treatment: Treatment) -> bool:
    """Whether a supplied value is the one behind a stored credential.

    This works for every treatment, including the one that cannot be read back:
    verifying is what a one-way treatment is for.
    """

    if stored is None:
        return False
    stored = str(stored)
    if treatment.mode is AtRest.HASH:
        if not stored.startswith(_HASH_MARKER):
            return False
        _, iterations, salt, digest = stored.split("$", 3)
        expected = hashlib.pbkdf2_hmac(
            "sha256", candidate.encode(), base64.b64decode(salt), int(iterations)
        )
        return hmac.compare_digest(expected, base64.b64decode(digest))
    return hmac.compare_digest(candidate, str(reveal(stored, treatment) or ""))


def reveal(stored: Any, treatment: Treatment) -> str | None:
    """The original value behind a stored credential, inside this layer only.

    Nothing above this layer calls it, and a one-way treatment refuses it
    outright rather than returning something that looks like an answer.
    """

    if stored is None:
        return None
    if not treatment.recoverable:
        raise CredentialError(
            f"{treatment.field!r} is held under a treatment that cannot be undone"
        )
    stored = str(stored)
    if treatment.mode is AtRest.PLAINTEXT:
        return stored
    if not stored.startswith(_ENCRYPTED_MARKER):
        raise CredentialError(f"{treatment.field!r} is not stored in the expected form")
    try:
        return _key().decrypt(stored[len(_ENCRYPTED_MARKER) :].encode()).decode()
    except InvalidToken as error:
        raise CredentialError(
            f"{treatment.field!r} cannot be read with the supplied key material"
        ) from error


def is_stored_form(value: Any) -> bool:
    """Whether a value is the stored form of a credential rather than a value."""

    return isinstance(value, str) and value.startswith((_HASH_MARKER, _ENCRYPTED_MARKER))


__all__ = [
    "AtRest",
    "CredentialError",
    "Treatment",
    "is_stored_form",
    "matches",
    "protect",
    "resolve",
    "reveal",
    "treatments",
]
