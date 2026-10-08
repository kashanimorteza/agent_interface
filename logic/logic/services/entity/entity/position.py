"""The Position Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Position(BaseEntity):
    _entity = model.Position
