"""Trading Platform Logic (task P3-G4-T2)."""

from __future__ import annotations

from ..model_interface import TradingPlatform
from .foundation import ModelLogicBase


class TradingPlatformLogic(ModelLogicBase[TradingPlatform]):
    model_cls = TradingPlatform
