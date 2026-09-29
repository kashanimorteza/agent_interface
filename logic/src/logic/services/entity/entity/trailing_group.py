"""Child Service for the TrailingGroup Entity."""

from model.interface import TrailingGroup

from logic.services.entity.base_entity import BaseEntity


class TrailingGroupService(BaseEntity):
    """Entity-bound Actions for TrailingGroup records."""

    entity = TrailingGroup
