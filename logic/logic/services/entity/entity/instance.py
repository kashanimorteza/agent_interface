"""Instance: the Child Service bound to the Instance Entity."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Instance(BaseEntity):
    """Works on Instance records through Storage without passing the Entity."""

    _entity = model.Instance
