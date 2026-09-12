"""Application Behaviour: one separately defined Logic unit per persistent Model."""

from __future__ import annotations

from ._base import ModelLogic
from .registry import REGISTRY

__all__ = ["ModelLogic", "REGISTRY"]
