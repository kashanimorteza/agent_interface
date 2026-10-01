"""Child Service of the Action Entity."""

from model import interface as model

from logic.services.entity.base_entity import BaseEntity


class Action(BaseEntity):
    """The Entity Actions bound to the Action Entity."""

    _entity = model.Action
