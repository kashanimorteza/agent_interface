from __future__ import annotations

from my_model import TrailingRule

from ._base import ModelLogic


class TrailingRuleLogic(ModelLogic[TrailingRule]):
    model_cls = TrailingRule
