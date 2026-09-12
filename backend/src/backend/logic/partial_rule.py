"""The Partial Rule Model's Logic unit."""

from __future__ import annotations

import my_model as m

from ._base import ModelLogic


class PartialRuleLogic(ModelLogic[m.PartialRule]):
    model_type = m.PartialRule
