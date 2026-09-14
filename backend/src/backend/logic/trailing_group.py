"""Trailing Group Logic (task P3-G7-T1)."""

from __future__ import annotations

from ..model_interface import TrailingGroup
from .foundation import ModelLogicBase


class TrailingGroupLogic(ModelLogicBase[TrailingGroup]):
    model_cls = TrailingGroup
