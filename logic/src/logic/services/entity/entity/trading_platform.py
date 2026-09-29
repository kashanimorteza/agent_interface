"""The TradingPlatform Service."""

from model.interface import TradingPlatform

from logic.services.entity.base import EntityServiceBase


class TradingPlatformService(EntityServiceBase[TradingPlatform]):
    """Entity-bound Actions for TradingPlatform records."""

    entity = TradingPlatform
