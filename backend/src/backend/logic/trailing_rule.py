"""Trailing Rule Logic (task P3-G7-T2)."""

from __future__ import annotations

from ..model_interface import TrailingRule
from .foundation import ModelLogicBase


class TrailingRuleLogic(ModelLogicBase[TrailingRule]):
    model_cls = TrailingRule
