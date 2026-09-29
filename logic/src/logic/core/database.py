"""The one shared handle Storage Service uses to reach Database's published surface."""

from functools import cache

from database.interface import Database


@cache
def gateway() -> Database:
    """Return the shared Database access surface, created on first use."""
    return Database()
