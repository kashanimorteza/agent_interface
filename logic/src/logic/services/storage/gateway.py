"""Storage Service's only route to Database Interface."""

from functools import cache

from database.interface import Database


@cache
def database() -> Database:
    """Return the shared Database access surface, created on first use."""
    return Database()
