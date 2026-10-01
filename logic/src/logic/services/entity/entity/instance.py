"""Child Service of the Instance Entity."""

from model import interface as model

from logic.services.entity.base_entity import BaseEntity


class Instance(BaseEntity):
    """The Entity Actions bound to the Instance Entity."""

    _entity = model.Instance
