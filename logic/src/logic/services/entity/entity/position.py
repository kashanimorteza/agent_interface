"""Child Service of the Position Entity."""

from model.interface import Position

from logic.services.entity.base_entity import BaseEntity


class PositionService(BaseEntity):
    """The Entity Actions bound to the Position Entity."""

    _entity = Position
