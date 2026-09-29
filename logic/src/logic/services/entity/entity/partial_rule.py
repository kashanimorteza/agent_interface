"""Entity Child Service bound to Model's Partial Rule Entity."""

from model.interface import PartialRule

from logic.services.entity.base_entity import BaseEntity


class PartialRuleService(BaseEntity):
    """Selects Partial Rule once and offers every shared Entity Action for it."""

    entity = PartialRule
