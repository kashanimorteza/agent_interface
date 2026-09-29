"""The TrailingRule Service."""

from model.interface import TrailingRule

from logic.services.entity.base import EntityServiceBase


class TrailingRuleService(EntityServiceBase[TrailingRule]):
    """Entity-bound Actions for TrailingRule records."""

    entity = TrailingRule
