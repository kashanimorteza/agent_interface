"""Child Service of the Partial Group Entity."""

from model import interface as model

from logic.services.entity.base_entity import BaseEntity


class PartialGroup(BaseEntity):
    """The Entity Actions bound to the Partial Group Entity."""

    _entity = model.PartialGroup
