"""Child Service of the Instance Entity."""

from model.interface import Instance

from logic.services.entity.base_entity import BaseEntity


class InstanceService(BaseEntity):
    """The Entity Actions bound to the Instance Entity."""

    _entity = Instance
