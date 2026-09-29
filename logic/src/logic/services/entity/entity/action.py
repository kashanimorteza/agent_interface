"""Child Service for the Action Entity."""

from model.interface import Action

from logic.services.entity.base_entity import BaseEntity


class ActionService(BaseEntity):
    """Entity-bound Actions for Action records."""

    entity = Action
