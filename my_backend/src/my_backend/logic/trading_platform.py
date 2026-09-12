from my_backend._model_interface import trading_platform
from my_backend.logic._base import ModelLogic


class TradingPlatformLogic(ModelLogic[trading_platform.TradingPlatform]):
    model_cls = trading_platform.TradingPlatform
