"""The Action Model's Logic unit."""

from __future__ import annotations

import my_model as m

from ._base import ModelLogic


class ActionLogic(ModelLogic[m.Action]):
    model_type = m.Action
