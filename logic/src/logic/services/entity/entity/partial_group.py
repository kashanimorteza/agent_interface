"""Child Service for the PartialGroup Entity."""

from model.interface import PartialGroup

from logic.services.entity.base_entity import BaseEntity


class PartialGroupService(BaseEntity):
    """Entity-bound Actions for PartialGroup records."""

    entity = PartialGroup
