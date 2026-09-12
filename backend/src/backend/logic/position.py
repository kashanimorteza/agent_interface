"""The Position Model's Logic unit."""

from __future__ import annotations

import my_model as m

from ._base import ModelLogic


class PositionLogic(ModelLogic[m.Position]):
    model_type = m.Position
