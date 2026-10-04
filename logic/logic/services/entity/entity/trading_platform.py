"""Entity Service Child for TradingPlatform."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class TradingPlatform(BaseEntity[model.TradingPlatform]):
    """The Child Service of the TradingPlatform Entity."""

    _entity = model.TradingPlatform
