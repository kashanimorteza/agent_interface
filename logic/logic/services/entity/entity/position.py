"""The Position Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Position(BaseEntity):
    """The Actions of the Position Entity."""

    _entity = model.Position
