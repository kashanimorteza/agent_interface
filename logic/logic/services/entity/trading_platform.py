"""The Trading Platform Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class TradingPlatform(BaseEntity):
    """The Actions of the Trading Platform Entity."""

    _entity = model.TradingPlatform
