"""Partial Rule Logic (task P3-G7-T4)."""

from __future__ import annotations

from ..model_interface import PartialRule
from .foundation import ModelLogicBase


class PartialRuleLogic(ModelLogicBase[PartialRule]):
    model_cls = PartialRule
