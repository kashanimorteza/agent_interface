"""Entity Child Service bound to Model's Trailing Rule Entity."""

from model.interface import TrailingRule

from logic.services.entity.base_entity import BaseEntity


class TrailingRuleService(BaseEntity):
    """Selects Trailing Rule once and offers every shared Entity Action for it."""

    entity = TrailingRule
