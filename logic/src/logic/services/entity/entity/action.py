"""Child Service of the Action Entity."""

from model.interface import Action

from logic.services.entity.base_entity import BaseEntity


class ActionService(BaseEntity):
    """The Entity Actions bound to the Action Entity."""

    _entity = Action
