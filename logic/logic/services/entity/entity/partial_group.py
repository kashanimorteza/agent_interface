"""The PartialGroup Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class PartialGroup(BaseEntity):
    """The Actions of the PartialGroup Entity."""

    _entity = model.PartialGroup
