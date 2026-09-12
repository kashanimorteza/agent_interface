from my_backend._model_interface import instance
from my_backend.logic._base import ModelLogic


class InstanceLogic(ModelLogic[instance.Instance]):
    model_cls = instance.Instance
