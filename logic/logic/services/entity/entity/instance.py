"""The Instance Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Instance(BaseEntity):
    """Child Service of the Instance Entity."""

    _entity = model.Instance
