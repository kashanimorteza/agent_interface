"""The Partial Group Model's Logic unit."""

from __future__ import annotations

import my_model as m

from ._base import ModelLogic


class PartialGroupLogic(ModelLogic[m.PartialGroup]):
    model_type = m.PartialGroup
