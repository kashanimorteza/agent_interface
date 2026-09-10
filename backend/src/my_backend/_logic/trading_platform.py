from __future__ import annotations

from my_model import TradingPlatform

from ._base import ModelLogic


class TradingPlatformLogic(ModelLogic[TradingPlatform]):
    model_cls = TradingPlatform
