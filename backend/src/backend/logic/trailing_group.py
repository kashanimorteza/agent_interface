"""The Trailing Group Model's Logic unit."""

from __future__ import annotations

import my_model as m

from ._base import ModelLogic


class TrailingGroupLogic(ModelLogic[m.TrailingGroup]):
    model_type = m.TrailingGroup
