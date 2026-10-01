"""Child Service of the Trailing Rule Entity."""

from model import interface as model

from logic.services.entity.base_entity import BaseEntity


class TrailingRule(BaseEntity):
    """The Entity Actions bound to the Trailing Rule Entity."""

    _entity = model.TrailingRule
