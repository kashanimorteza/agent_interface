"""Logic of the Trading Platform Model."""

from my_model import TradingPlatform

from ..base import ModelLogic


class TradingPlatformLogic(ModelLogic[TradingPlatform]):
    model = TradingPlatform
