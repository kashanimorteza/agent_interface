"""The Position Service."""

from model.interface import Position

from logic.services.entity.base import EntityServiceBase


class PositionService(EntityServiceBase[Position]):
    """Entity-bound Actions for Position records."""

    entity = Position
