"""The User Adapter."""

from logic.interface import Entity

from api.endpoints import Adapter

router = Adapter(Entity.Service.User)
