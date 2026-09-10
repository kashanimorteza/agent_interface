from __future__ import annotations

from my_model import Position

from ._base import ModelLogic


class PositionLogic(ModelLogic[Position]):
    model_cls = Position
