"""Database Interface — the only layer published to consumers: Model
operations plus Instance discovery and selection."""

from .gateway import Database
from .registry import InstanceIdentity, InstanceRegistry

__all__ = ["Database", "InstanceIdentity", "InstanceRegistry"]
