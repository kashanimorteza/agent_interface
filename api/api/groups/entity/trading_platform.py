"""The Trading Platform Adapter."""

from logic.interface import Entity

from api.endpoints import Adapter

router = Adapter(Entity.Service.TradingPlatform)
