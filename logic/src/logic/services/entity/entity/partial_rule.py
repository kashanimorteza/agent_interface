"""The PartialRule Service."""

from model.interface import PartialRule

from logic.services.entity.base import EntityServiceBase


class PartialRuleService(EntityServiceBase[PartialRule]):
    """Entity-bound Actions for PartialRule records."""

    entity = PartialRule
