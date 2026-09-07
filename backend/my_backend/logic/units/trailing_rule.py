"""Logic of the Trailing Rule Model."""

from my_model import TrailingRule

from ..base import ModelLogic


class TrailingRuleLogic(ModelLogic[TrailingRule]):
    model = TrailingRule
