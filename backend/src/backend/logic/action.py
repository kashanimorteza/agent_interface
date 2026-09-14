"""Action Logic (task P3-G8-T2)."""

from __future__ import annotations

from ..model_interface import Action
from .foundation import ModelLogicBase


class ActionLogic(ModelLogicBase[Action]):
    model_cls = Action
