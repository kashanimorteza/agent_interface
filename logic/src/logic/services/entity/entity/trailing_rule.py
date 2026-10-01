"""Child Service of the Trailing Rule Entity."""

from model.interface import TrailingRule

from logic.services.entity.base_entity import BaseEntity


class TrailingRuleService(BaseEntity):
    """The Entity Actions bound to the Trailing Rule Entity."""

    _entity = TrailingRule
