"""Child Service of the Position Entity."""

from model import interface as model

from logic.services.entity.base_entity import BaseEntity


class Position(BaseEntity):
    """The Entity Actions bound to the Position Entity."""

    _entity = model.Position
