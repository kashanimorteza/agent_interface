from __future__ import annotations

from my_model import ActionGroup

from ._base import ModelLogic


class ActionGroupLogic(ModelLogic[ActionGroup]):
    model_cls = ActionGroup
