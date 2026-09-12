from my_backend._model_interface import action_group
from my_backend.logic._base import ModelLogic


class ActionGroupLogic(ModelLogic[action_group.ActionGroup]):
    model_cls = action_group.ActionGroup
