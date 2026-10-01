"""Child Service of the Partial Rule Entity."""

from model import interface as model

from logic.services.entity.base_entity import BaseEntity


class PartialRule(BaseEntity):
    """The Entity Actions bound to the Partial Rule Entity."""

    _entity = model.PartialRule
