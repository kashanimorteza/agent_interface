from __future__ import annotations

from my_model import PartialGroup

from ._base import ModelLogic


class PartialGroupLogic(ModelLogic[PartialGroup]):
    model_cls = PartialGroup
