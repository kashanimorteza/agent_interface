"""The Trailing Rule Model's Logic unit."""

from __future__ import annotations

import my_model as m

from ._base import ModelLogic


class TrailingRuleLogic(ModelLogic[m.TrailingRule]):
    model_type = m.TrailingRule
