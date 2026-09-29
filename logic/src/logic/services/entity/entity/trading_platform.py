"""Child Service for the TradingPlatform Entity."""

from model.interface import TradingPlatform

from logic.services.entity.base_entity import BaseEntity


class TradingPlatformService(BaseEntity):
    """Entity-bound Actions for TradingPlatform records."""

    entity = TradingPlatform
