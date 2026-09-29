"""Child Service for the TrailingRule Entity."""

from model.interface import TrailingRule

from logic.services.entity.base_entity import BaseEntity


class TrailingRuleService(BaseEntity):
    """Entity-bound Actions for TrailingRule records."""

    entity = TrailingRule
