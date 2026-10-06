"""The Trading Platform Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class TradingPlatform(BaseEntity):
    """Child Service of the Trading Platform Entity."""

    _entity = model.TradingPlatform
