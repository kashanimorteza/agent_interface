from __future__ import annotations

from my_model import PartialRule

from ._base import ModelLogic


class PartialRuleLogic(ModelLogic[PartialRule]):
    model_cls = PartialRule
