"""The Action Service."""

from model.interface import Action

from logic.services.entity.base import EntityServiceBase


class ActionService(EntityServiceBase[Action]):
    """Entity-bound Actions for Action records."""

    entity = Action
