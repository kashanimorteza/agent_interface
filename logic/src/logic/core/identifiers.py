"""Validation of the names Logic realizes as identifiers."""

import keyword
import re
from collections.abc import Callable, Iterable

from logic.core.errors import ConfigurationError


def snake_case(name: str) -> str:
    """Normalize a name to snake_case.

    Args:
        name (str): Name to normalize.

    Returns:
        (str): Lowercase words joined by single underscores.
    """
    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name.strip())
    return re.sub(r"[^A-Za-z0-9]+", "_", spaced).strip("_").lower()


def pascal_case(name: str) -> str:
    """Normalize a name to PascalCase.

    Args:
        name (str): Name to normalize.

    Returns:
        (str): Capitalized words joined without separators.
    """
    return "".join(word.capitalize() for word in snake_case(name).split("_"))


def check_identifiers(
    names: Iterable[str],
    kind: str = "identifier",
    normalize: Callable[[str], str] = snake_case,
) -> tuple[str, ...]:
    """Check that names are valid, non-reserved, and unique after normalization.

    Args:
        names (Iterable[str]): Configured names to check.
        kind (str): What the names identify, used in error messages.
        normalize (Callable[[str], str]): Declared normalization of the selected language.

    Returns:
        (tuple[str, ...]): The normalized names, in order.
    """
    seen: dict[str, str] = {}
    for name in names:
        normalized = normalize(name)
        if not normalized.isidentifier() or keyword.iskeyword(normalized):
            raise ConfigurationError(
                f"{kind} '{name}' is not a valid identifier ('{normalized}')"
            )
        if normalized in seen:
            raise ConfigurationError(
                f"{kind} '{name}' collides with '{seen[normalized]}' after normalization"
            )
        seen[normalized] = name
    return tuple(seen)
