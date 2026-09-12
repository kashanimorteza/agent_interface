"""The Action Group Model's Logic unit."""

from __future__ import annotations

import my_model as m

from ._base import ModelLogic


class ActionGroupLogic(ModelLogic[m.ActionGroup]):
    model_type = m.ActionGroup
