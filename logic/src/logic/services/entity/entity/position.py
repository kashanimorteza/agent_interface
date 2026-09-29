"""Entity Child Service bound to Model's Position Entity."""

from model.interface import Position

from logic.services.entity.base_entity import BaseEntity


class PositionService(BaseEntity):
    """Selects Position once and offers every shared Entity Action for it."""

    entity = Position
