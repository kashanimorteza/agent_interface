from my_backend._model_interface import position
from my_backend.logic._base import ModelLogic


class PositionLogic(ModelLogic[position.Position]):
    model_cls = position.Position
