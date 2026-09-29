"""Entity Child Service bound to Model's Partial Group Entity."""

from model.interface import PartialGroup

from logic.services.entity.base_entity import BaseEntity


class PartialGroupService(BaseEntity):
    """Selects Partial Group once and offers every shared Entity Action for it."""

    entity = PartialGroup
