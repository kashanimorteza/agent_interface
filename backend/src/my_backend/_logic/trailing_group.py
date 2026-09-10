from __future__ import annotations

from my_model import TrailingGroup

from ._base import ModelLogic


class TrailingGroupLogic(ModelLogic[TrailingGroup]):
    model_cls = TrailingGroup
