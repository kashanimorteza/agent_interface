"""The Trading Platform Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class TradingPlatform(BaseEntity):
    _entity = model.TradingPlatform
