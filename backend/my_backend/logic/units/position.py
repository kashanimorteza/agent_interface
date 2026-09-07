"""Logic of the Position Model."""

from my_model import Position

from ..base import ModelLogic


class PositionLogic(ModelLogic[Position]):
    model = Position
