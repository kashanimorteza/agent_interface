from my_backend._model_interface import trailing_rule
from my_backend.logic._base import ModelLogic


class TrailingRuleLogic(ModelLogic[trailing_rule.TrailingRule]):
    model_cls = trailing_rule.TrailingRule
