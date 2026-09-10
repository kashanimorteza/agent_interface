from __future__ import annotations

from my_model import Instance

from ._base import ModelLogic


class InstanceLogic(ModelLogic[Instance]):
    model_cls = Instance
