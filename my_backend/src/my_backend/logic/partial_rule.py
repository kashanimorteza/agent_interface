from my_backend._model_interface import partial_rule
from my_backend.logic._base import ModelLogic


class PartialRuleLogic(ModelLogic[partial_rule.PartialRule]):
    model_cls = partial_rule.PartialRule
