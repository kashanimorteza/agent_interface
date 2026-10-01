"""Child Service of the Partial Group Entity."""

from model.interface import PartialGroup

from logic.services.entity.base_entity import BaseEntity


class PartialGroupService(BaseEntity):
    """The Entity Actions bound to the Partial Group Entity."""

    _entity = PartialGroup
