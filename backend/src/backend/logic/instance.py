"""Instance Logic (task P3-G4-T3)."""

from __future__ import annotations

from ..model_interface import Instance
from .foundation import ModelLogicBase


class InstanceLogic(ModelLogicBase[Instance]):
    model_cls = Instance
