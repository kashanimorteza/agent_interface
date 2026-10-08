"""TradingPlatform: the Child Service bound to the Trading Platform Entity."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class TradingPlatform(BaseEntity):
    """Works on Trading Platform records through Storage without passing the Entity."""

    _entity = model.TradingPlatform
