"""The ActionGroup Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class ActionGroup(BaseEntity):
    """The Actions of the ActionGroup Entity."""

    _entity = model.ActionGroup
