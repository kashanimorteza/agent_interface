from my_backend._model_interface import action
from my_backend.logic._base import ModelLogic


class ActionLogic(ModelLogic[action.Action]):
    model_cls = action.Action
