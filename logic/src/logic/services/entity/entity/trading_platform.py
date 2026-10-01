"""Child Service of the Trading Platform Entity."""

from model.interface import TradingPlatform

from logic.services.entity.base_entity import BaseEntity


class TradingPlatformService(BaseEntity):
    """The Entity Actions bound to the Trading Platform Entity."""

    _entity = TradingPlatform
