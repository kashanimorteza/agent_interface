"""Engine implementations: one isolated module per Engine marked for implementation."""

from importlib import import_module
from typing import Any

IMPLEMENTED = ("sqlite",)


def load(key: str) -> Any:
    """Return the implementation class of an Engine.

    Args:
        key (str): Key of an Engine marked for implementation.

    Returns:
        (Any): The `Engine` class of that Engine's implementation module.
    """
    return import_module(f"database.engine.{key}").Engine
