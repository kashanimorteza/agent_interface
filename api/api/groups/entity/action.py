"""The Action Adapter."""

from logic.interface import Entity

from api.endpoints import Adapter

router = Adapter(Entity.Service.Action)
