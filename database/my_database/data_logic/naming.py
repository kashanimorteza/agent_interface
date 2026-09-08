"""How a definition's name becomes a name in storage.

These are physical naming choices and nothing more: they decide what a table is
called, never what it means. The meaning stays with the definition.
"""

from __future__ import annotations

import re

_SIBILANT = ("s", "x", "z", "ch", "sh")


def snake_case(name: str) -> str:
    """``TradingPlatform`` becomes ``trading_platform``."""

    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", "_", name)
    return spaced.lower()


def plural(word: str) -> str:
    """The plural of one snake_case word, for the table a definition becomes."""

    if word.endswith("y") and not word.endswith(("ay", "ey", "iy", "oy", "uy")):
        return f"{word[:-1]}ies"
    if word.endswith(_SIBILANT):
        return f"{word}es"
    return f"{word}s"


def table_name(entity_name: str) -> str:
    """The table one definition maps to."""

    parts = snake_case(entity_name).split("_")
    return "_".join([*parts[:-1], plural(parts[-1])])


def index_name(table: str, column: str) -> str:
    return f"ix_{table}_{column}"


def unique_constraint_name(table: str, columns: tuple[str, ...]) -> str:
    return f"uq_{table}_{'_'.join(columns)}"
