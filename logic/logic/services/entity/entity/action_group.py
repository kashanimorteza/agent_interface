"""ActionGroup: the Child Service bound to the Action Group Entity."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class ActionGroup(BaseEntity):
    """Works on Action Group records through Storage without passing the Entity."""

    _entity = model.ActionGroup
