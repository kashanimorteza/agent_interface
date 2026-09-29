"""Child Service for the Position Entity."""

from model.interface import Position

from logic.services.entity.base_entity import BaseEntity


class PositionService(BaseEntity):
    """Entity-bound Actions for Position records."""

    entity = Position
