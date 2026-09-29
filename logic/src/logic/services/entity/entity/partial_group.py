"""The PartialGroup Service."""

from model.interface import PartialGroup

from logic.services.entity.base import EntityServiceBase


class PartialGroupService(EntityServiceBase[PartialGroup]):
    """Entity-bound Actions for PartialGroup records."""

    entity = PartialGroup
