"""The Action Group Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class ActionGroup(BaseEntity):
    """The Actions of the Action Group Entity."""

    _entity = model.ActionGroup
