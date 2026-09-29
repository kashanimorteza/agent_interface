"""Child Service for the PartialRule Entity."""

from model.interface import PartialRule

from logic.services.entity.base_entity import BaseEntity


class PartialRuleService(BaseEntity):
    """Entity-bound Actions for PartialRule records."""

    entity = PartialRule
