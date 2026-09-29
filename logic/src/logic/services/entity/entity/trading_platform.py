"""Entity Child Service bound to Model's Trading Platform Entity."""

from model.interface import TradingPlatform

from logic.services.entity.base_entity import BaseEntity


class TradingPlatformService(BaseEntity):
    """Selects Trading Platform once and offers every shared Entity Action for it."""

    entity = TradingPlatform
