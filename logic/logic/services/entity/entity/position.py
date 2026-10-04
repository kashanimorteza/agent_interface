"""Entity Service Child for Position."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Position(BaseEntity[model.Position]):
    """The Child Service of the Position Entity."""

    _entity = model.Position
