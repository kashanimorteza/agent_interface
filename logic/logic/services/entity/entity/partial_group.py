"""PartialGroup: the Child Service bound to the Partial Group Entity."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class PartialGroup(BaseEntity):
    """Works on Partial Group records through Storage without passing the Entity."""

    _entity = model.PartialGroup
