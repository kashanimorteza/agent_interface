"""Shared validation of the identities that Logic publishes."""

import keyword
import unicodedata
from collections.abc import Iterable

from logic.core.errors import ConfigurationError


class IdentityError(ConfigurationError):
    """A configured identity is invalid, reserved, or collides with another."""


def validate_identities(identities: Iterable[str]) -> None:
    """Reject identities that are invalid, reserved, or equal after normalization.

    Every problem found is reported together in one error that names each offending
    value. A rejected identity is never repaired, suffixed, or renamed.

    Args:
        identities (Iterable[str]): The identities that must be unique together.
    """
    problems: list[str] = []
    seen: dict[str, str] = {}
    for identity in identities:
        normalized = unicodedata.normalize("NFKC", identity)
        if not normalized.isidentifier():
            problems.append(f"{identity!r} is not a valid identifier")
        elif keyword.iskeyword(normalized):
            problems.append(f"{identity!r} is a reserved word")
        elif normalized in seen:
            problems.append(
                f"{identity!r} and {seen[normalized]!r} are the same identity {normalized!r}"
            )
        else:
            seen[normalized] = identity
    if problems:
        raise IdentityError("; ".join(problems) + ".")
