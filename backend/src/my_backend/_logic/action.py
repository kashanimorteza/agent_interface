from __future__ import annotations

from my_model import Action

from ._base import ModelLogic


class ActionLogic(ModelLogic[Action]):
    model_cls = Action
