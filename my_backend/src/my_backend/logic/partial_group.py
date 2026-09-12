from my_backend._model_interface import partial_group
from my_backend.logic._base import ModelLogic


class PartialGroupLogic(ModelLogic[partial_group.PartialGroup]):
    model_cls = partial_group.PartialGroup
