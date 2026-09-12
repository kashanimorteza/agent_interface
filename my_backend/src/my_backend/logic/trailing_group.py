from my_backend._model_interface import trailing_group
from my_backend.logic._base import ModelLogic


class TrailingGroupLogic(ModelLogic[trailing_group.TrailingGroup]):
    model_cls = trailing_group.TrailingGroup
