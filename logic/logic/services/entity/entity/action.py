"""Action: the Child Service bound to the Action Entity."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Action(BaseEntity):
    """Works on Action records through Storage without passing the Entity."""

    _entity = model.Action
