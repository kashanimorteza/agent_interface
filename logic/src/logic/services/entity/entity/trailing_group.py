"""The TrailingGroup Service."""

from model.interface import TrailingGroup

from logic.services.entity.base import EntityServiceBase


class TrailingGroupService(EntityServiceBase[TrailingGroup]):
    """Entity-bound Actions for TrailingGroup records."""

    entity = TrailingGroup
