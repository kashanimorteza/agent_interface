"""Position Logic (task P3-G8-T3)."""

from __future__ import annotations

from ..model_interface import Position
from .foundation import ModelLogicBase


class PositionLogic(ModelLogicBase[Position]):
    model_cls = Position
