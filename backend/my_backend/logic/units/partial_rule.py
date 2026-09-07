"""Logic of the Partial Rule Model."""

from my_model import PartialRule

from ..base import ModelLogic


class PartialRuleLogic(ModelLogic[PartialRule]):
    model = PartialRule
