"""Partial Group Logic (task P3-G7-T3)."""

from __future__ import annotations

from ..model_interface import PartialGroup
from .foundation import ModelLogicBase


class PartialGroupLogic(ModelLogicBase[PartialGroup]):
    model_cls = PartialGroup
