"""The Trailing Rule Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class TrailingRule(BaseEntity):
    """The Actions of the Trailing Rule Entity."""

    _entity = model.TrailingRule
