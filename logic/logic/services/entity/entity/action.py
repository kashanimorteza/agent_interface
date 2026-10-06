"""The Action Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Action(BaseEntity):
    """Child Service of the Action Entity."""

    _entity = model.Action
