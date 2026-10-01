"""Child Service of the Partial Rule Entity."""

from model.interface import PartialRule

from logic.services.entity.base_entity import BaseEntity


class PartialRuleService(BaseEntity):
    """The Entity Actions bound to the Partial Rule Entity."""

    _entity = PartialRule
