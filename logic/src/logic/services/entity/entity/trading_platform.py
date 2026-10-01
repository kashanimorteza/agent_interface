"""Child Service of the Trading Platform Entity."""

from model import interface as model

from logic.services.entity.base_entity import BaseEntity


class TradingPlatform(BaseEntity):
    """The Entity Actions bound to the Trading Platform Entity."""

    _entity = model.TradingPlatform
