"""Position: the Child Service bound to the Position Entity."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Position(BaseEntity):
    """Works on Position records through Storage without passing the Entity."""

    _entity = model.Position
