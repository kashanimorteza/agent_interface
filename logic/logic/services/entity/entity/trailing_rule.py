"""The TrailingRule Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class TrailingRule(BaseEntity):
    """The Actions of the TrailingRule Entity."""

    _entity = model.TrailingRule
