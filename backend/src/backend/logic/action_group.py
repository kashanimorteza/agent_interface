"""Action Group Logic (task P3-G8-T1)."""

from __future__ import annotations

from ..model_interface import ActionGroup
from .foundation import ModelLogicBase


class ActionGroupLogic(ModelLogicBase[ActionGroup]):
    model_cls = ActionGroup
